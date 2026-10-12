#!/usr/bin/env python3
"""Optional, dependency-free single-file picker. Never reads a model-supplied PDF path."""

import argparse
import hashlib
import json
import os
import secrets
import stat
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path
from uuid import UUID

MAX_BYTES = 30 * 1024 * 1024
SAFE_ERRORS = {
    "File selection cancelled.",
    "Native file picker unavailable. Use PRDB web Upload instead.",
    "No native picker is available. Use PRDB web Upload instead.",
    "Select a regular PDF, without symlinks.",
    "PDF must be a regular file up to 30 MiB.",
    "The selected file is not a PDF up to 30 MiB.",
    "Upload confirmation timed out. No new ticket was created.",
}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise ValueError("PRDB did not accept the configured endpoint. Redirects are disabled.")


def read_ticket(path):
    path = Path(path).absolute()
    if any(p.is_symlink() for p in [path, *path.parents]):
        raise ValueError("Ticket must be a private regular file, without symlinks.")
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode) != 0o600 or info.st_size > 4096:
        raise ValueError("Ticket must be at most 4096 bytes, with permissions 600.")
    ticket = json.loads(path.read_text())
    origin = urllib.parse.urlsplit(ticket["origin"])
    valid = (
        origin.scheme == "https"
        and origin.hostname in {"prdb.ai", "prdbtest.app"}
        and origin.port in {None, 443}
    )
    valid |= origin.scheme == "http" and origin.hostname in {"127.0.0.1", "localhost"}
    if (
        not valid
        or origin.username
        or origin.password
        or origin.path
        or origin.query
        or origin.fragment
    ):
        raise ValueError("Unexpected PRDB origin.")
    ticket["upload_id"] = str(UUID(ticket["upload_id"]))
    secret = ticket["upload_token"]
    if not isinstance(secret, str) or not secret.startswith("prdb_upload_") or len(secret) > 200:
        raise ValueError("Invalid ticket.")
    return ticket


def select_pdf():
    if sys.platform == "darwin":
        result = subprocess.run(
            [
                "osascript",
                "-e",
                # Show files even without macOS UTI metadata. PDF validity is
                # checked against actual bytes after the human selects a file.
                'POSIX path of (choose file with prompt "Select the PDF you want to upload privately to PRDB" default location (path to downloads folder))',
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            if "(-128)" in result.stderr:
                raise ValueError("File selection cancelled.")
            raise ValueError("Native file picker unavailable. Use PRDB web Upload instead.")
        selected = result.stdout.strip()
    else:
        try:
            import tkinter
            from tkinter import filedialog

            root = tkinter.Tk()
            root.withdraw()
            selected = filedialog.askopenfilename(
                title="Select your private PRDB PDF", filetypes=[("PDF", "*.pdf")]
            )
            root.destroy()
        except ImportError as exc:
            raise ValueError("No native picker is available. Use PRDB web Upload instead.") from exc
    if not selected:
        raise ValueError("File selection cancelled.")
    return Path(selected).absolute()


def snapshot(selected):
    if any(p.is_symlink() for p in [selected, *selected.parents]):
        raise ValueError("Select a regular PDF, without symlinks.")
    descriptor = os.open(selected, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    with os.fdopen(descriptor, "rb") as source:
        info = os.fstat(source.fileno())
        if not stat.S_ISREG(info.st_mode) or not 5 <= info.st_size <= MAX_BYTES:
            raise ValueError("PDF must be a regular file up to 30 MiB.")
        data = source.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES or not data.startswith(b"%PDF-"):
        raise ValueError("The selected file is not a PDF up to 30 MiB.")
    return data


def call(ticket, action, payload=None, *, binary=None):
    headers = {"Authorization": "Bearer " + ticket["upload_token"]}
    data = None
    if binary is not None:
        boundary = secrets.token_hex(24)
        # Server stores the user-confirmed original filename from the proposal.
        data = (
            f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="selected.pdf"\r\nContent-Type: application/pdf\r\n\r\n'.encode()
            + binary
            + f"\r\n--{boundary}--\r\n".encode()
        )
        headers["Content-Type"] = "multipart/form-data; boundary=" + boundary
    elif payload is not None:
        data = json.dumps(payload).encode()
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(
        ticket["origin"] + "/api/v1/reading-transfer/" + ticket["upload_id"] + "/" + action,
        data=data,
        headers=headers,
    )
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    try:
        with opener.open(request, timeout=60) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        try:
            detail = json.load(exc).get("detail", "PRDB rejected the upload.")
        except (ValueError, AttributeError):
            detail = "PRDB rejected the upload."
        raise ValueError(str(detail)[:200]) from None


def run(ticket):
    selected = select_pdf()  # Never selectable by a model argument.
    data = snapshot(selected)
    proposal = {
        "filename": selected.name,
        "sha256": hashlib.sha256(data).hexdigest(),
        "byte_size": len(data),
    }
    call(ticket, "proposal", proposal)
    webbrowser.open(ticket["origin"] + "/connections/upload?request=" + ticket["upload_id"])
    deadline = time.monotonic() + 15 * 60
    while time.monotonic() < deadline:
        result = call(ticket, "status")
        if result["status"] == "uploaded":
            return result
        if result["status"] == "approved":
            # Exact immutable bytes; response-loss retry uses the same ticket/import.
            for attempt in range(3):
                try:
                    reply = call(ticket, "file", binary=data)
                    return {
                        "status": "uploaded",
                        "document_id": reply["document"]["id"],
                        "reader_path": reply["reader_path"],
                    }
                except (urllib.error.URLError, TimeoutError):
                    if attempt == 2:
                        raise ValueError(
                            "Upload response unavailable. Check get_pdf_upload before retrying."
                        ) from None
        time.sleep(2.5)
    raise ValueError("Upload confirmation timed out. No new ticket was created.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ticket", required=True, help="Private JSON picker_ticket, permissions 600"
    )
    args = parser.parse_args()
    try:
        print(json.dumps(run(read_ticket(args.ticket))))
    except (ValueError, OSError, KeyError, urllib.error.URLError) as exc:
        # Never print URLs/headers/exception traces that could contain credentials.
        message = str(exc)
        print(
            message
            if message in SAFE_ERRORS
            else "PRDB upload did not complete. Check the confirmation page or retry the same ticket.",
            file=sys.stderr,
        )
        sys.exit(1)
