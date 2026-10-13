#!/usr/bin/env python3
"""Transfer only files inside a root explicitly granted by the user/client."""

import argparse
import hashlib
import json
import os
import stat
import urllib.parse
import urllib.request
from pathlib import Path
from uuid import uuid4

MAX_PDF = 30 * 1024 * 1024


def selected(root, relative):
    root = Path(root).resolve(strict=True)
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError("Choose a relative file within the user-granted root.")
    current = root
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("Symlinks cannot expand the selected root.")
    resolved = current.resolve(strict=True)
    if not resolved.is_relative_to(root) or not resolved.is_file():
        raise ValueError("The selected file is outside the granted root.")
    directory_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in path.parts[:-1]:
            next_fd = os.open(
                part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory_fd
            )
            os.close(directory_fd)
            directory_fd = next_fd
        fd = os.open(
            path.parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory_fd
        )
    finally:
        os.close(directory_fd)
    with os.fdopen(fd, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError("Choose a regular PDF file.")
        data = stream.read(MAX_PDF + 1)
    if not data.startswith(b"%PDF-") or len(data) > MAX_PDF or b"%%EOF" not in data[-2048:]:
        raise ValueError("Choose a complete PDF of at most 30 MiB.")
    return resolved, data


def inspect(root, files=None):
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError("Choose a user-granted regular directory.")
    files = files or [
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() == ".pdf" and not p.is_symlink()
    ]
    if len(files) > 50:
        raise ValueError("Select at most 50 PDFs per task.")
    result = []
    total = 0
    for name in sorted(files):
        path, data = selected(root, name)
        total += len(data)
        if total > 300 * 1024 * 1024:
            raise ValueError("Select at most 300 MiB per task.")
        item = {
            "relative_file": name,
            "sha256": hashlib.sha256(data).hexdigest(),
            "size_bytes": len(data),
            "title": None,
            "text_preview": None,
        }
        try:
            import io

            from pypdf import PdfReader

            pdf = PdfReader(io.BytesIO(data))
            item["title"] = str((pdf.metadata or {}).get("/Title", ""))[:2000]
            item["text_preview"] = "\n".join(
                page.extract_text() or "" for page in list(pdf.pages)[:3]
            )[:12000]
        except ImportError:
            item["warning"] = (
                "metadata_reader_unavailable; use the client's PDF reader or browser import"
            )
        except Exception:
            item["warning"] = "metadata_unavailable; choose the target explicitly"
        result.append(item)
    return {"files": result, "total_bytes": total, "selected_count": len(result)}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def upload(root, relative, lease_file):
    lease_path = Path(lease_file)
    if (
        lease_path.is_symlink()
        or stat.S_IMODE(lease_path.stat().st_mode) != 0o600
        or lease_path.stat().st_size > 10000
    ):
        raise ValueError("Use a regular mode-600 lease file.")
    ticket = json.loads(lease_path.read_text())
    _, data = selected(root, relative)
    if hashlib.sha256(data).hexdigest() != ticket["sha256"]:
        raise ValueError("The selected PDF changed; prepare a fresh upload.")
    parsed = urllib.parse.urlsplit(ticket["transfer_url"])
    public = (
        parsed.scheme == "https"
        and parsed.hostname in {"prdb.ai", "prdbtest.app"}
        and parsed.port in {None, 443}
    )
    local = parsed.scheme == "http" and parsed.hostname in {"localhost", "127.0.0.1"}
    if (
        not (public or local)
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
        or parsed.path != f"/api/v1/reading-transfer/{ticket['handle']}/direct"
    ):
        raise ValueError("Use the fixed PRDB transfer endpoint.")
    boundary = "prdb-" + uuid4().hex
    # Constant filename avoids path/header injection; original local names remain local.
    body = (
        f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="selected.pdf"\r\nContent-Type: application/pdf\r\n\r\n'.encode()
        + data
        + f"\r\n--{boundary}--\r\n".encode()
    )
    request = urllib.request.Request(
        ticket["transfer_url"],
        data=body,
        headers={
            "Authorization": "Bearer " + ticket["transfer_lease"],
            "Content-Type": "multipart/form-data; boundary=" + boundary,
        },
    )
    with urllib.request.build_opener(NoRedirect()).open(request, timeout=60) as response:
        result = json.loads(response.read(256 * 1024))
    if not result.get("document", {}).get("id"):
        raise ValueError("Upload did not return a saved document.")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["inspect", "upload"])
    parser.add_argument("--root", required=True)
    parser.add_argument("--file", action="append")
    parser.add_argument("--lease-file")
    args = parser.parse_args()
    if args.action == "inspect":
        result = inspect(args.root, args.file)
    else:
        if not args.file or len(args.file) != 1 or not args.lease_file:
            parser.error("upload requires one relative --file and a private --lease-file")
        result = upload(args.root, args.file[0], args.lease_file)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
