#!/usr/bin/env python3
"""Bootstrap before OAuth; only fixed public/loopback origins and private receipts."""

import argparse
import http.cookiejar
import json
import os
import shutil
import stat
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from uuid import uuid4


def origin(value):
    parsed = urllib.parse.urlsplit(value)
    allowed = (
        parsed.scheme == "https"
        and parsed.hostname in {"prdb.ai", "prdbtest.app"}
        and parsed.port in {None, 443}
    )
    allowed |= parsed.scheme == "http" and parsed.hostname in {"localhost", "127.0.0.1"}
    if (
        not allowed
        or parsed.username
        or parsed.password
        or parsed.path
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("Use the installed PRDB origin or an explicit local test origin.")
    return value


def bundled_origin():
    root = Path(__file__).resolve().parents[3]
    path = root / ".mcp.json"
    if not path.exists():
        path = root / "mcp.json"
    url = json.loads(path.read_text())["mcpServers"]["prdb-reading"]["url"]
    return origin(url.removesuffix("/mcp"))


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Client:
    def __init__(self, base):
        self.base = origin(base)
        self.http = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()), NoRedirect()
        )

    def call(self, path, payload=None):
        headers = {"Accept": "application/json"}
        data = None
        if payload is not None:
            csrf = self.call("/auth/csrf")["csrfToken"]
            headers.update(
                {"X-CSRFToken": csrf, "Origin": self.base, "Content-Type": "application/json"}
            )
            data = json.dumps(payload).encode()
        request = urllib.request.Request(self.base + "/api/v1" + path, data=data, headers=headers)
        try:
            with self.http.open(request, timeout=15) as reply:
                return json.loads(reply.read(256 * 1024))
        except urllib.error.HTTPError as exc:
            raise ValueError(
                f"PRDB returned {exc.code}; check the browser or start setup again."
            ) from exc


def save_receipt(path, value):
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags, 0o600)
    with os.fdopen(fd, "w") as stream:
        json.dump(value, stream)


def read_receipt(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file() or stat.S_IMODE(path.stat().st_mode) != 0o600:
        raise ValueError("Use a regular mode-600 receipt file without symlinks.")
    if path.stat().st_size > 10000:
        raise ValueError("Invalid setup receipt.")
    return json.loads(path.read_text())


def diagnose(client):
    result = {"setup": client.call("/agent-onboarding"), "codex": {"available": False}}
    command = shutil.which("codex")
    if command:
        result["codex"]["available"] = True
        try:
            reply = subprocess.run(
                [command, "plugin", "list", "--json"],
                capture_output=True,
                text=True,
                timeout=10,
                check=True,
            )
            plugins = json.loads(reply.stdout)
            result["codex"]["prdb_plugins"] = [
                {k: item.get(k) for k in ("name", "version", "enabled", "installed")}
                for item in plugins.get("installed", [])
                if item.get("name") == "prdb"
            ]
        except (subprocess.SubprocessError, ValueError):
            result["codex"]["status"] = "plugin_diagnostics_unavailable"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["diagnose", "register", "status"])
    parser.add_argument("--origin")
    parser.add_argument("--receipt-file")
    args = parser.parse_args()
    base = origin(args.origin) if args.origin else bundled_origin()
    client = Client(base)
    if args.action == "diagnose":
        result = diagnose(client)
    elif not args.receipt_file:
        parser.error(
            "register/status need --receipt-file; never put a receipt in command arguments"
        )
    elif args.action == "register":
        # Check output before causing even a task-record side effect.
        if Path(args.receipt_file).exists():
            parser.error("Use a new receipt file")
        result = client.call("/agent-onboarding", {"request_key": str(uuid4())})
        receipt = result.pop("receipt")
        save_receipt(args.receipt_file, {"origin": base, "receipt": receipt})
    else:
        private = read_receipt(args.receipt_file)
        if origin(private["origin"]) != base:
            parser.error("Setup receipt belongs to a different PRDB environment")
        result = client.call("/agent-onboarding/status", {"receipt": private["receipt"]})
    print(json.dumps(result))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, urllib.error.URLError):
        raise SystemExit(
            "Setup could not complete. Check the fixed origin, client and private receipt; no credentials were changed."
        ) from None
