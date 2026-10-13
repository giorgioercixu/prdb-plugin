# Setup helper

`onboard.py` uses only Python's standard library. `diagnose` checks the bundled
origin, public setup status and available Codex plugin state without editing
client configuration. `register --receipt-file <new private file>` creates a
registration handoff; `status --receipt-file <file>` reports verification progress.
Passwords, email contents, OAuth tokens and admin permissions are never accepted.
Developer tests may explicitly select a loopback origin.

Recent update: 2026-10-13 Added local-first diagnostics and registration receipts.
