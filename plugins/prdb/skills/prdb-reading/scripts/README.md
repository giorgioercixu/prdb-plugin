# Optional PDF picker

`upload_pdf.py` is a dependency-free Python 3 helper for a **single human-selected PDF**. It accepts a short-lived private upload-ticket JSON, never a PDF path or URL. The macOS chooser defaults to Downloads; Windows/Linux need a Tk picker. Actual bytes are snapshotted and uploaded only after browser approval of file/hash/Paper.

```sh
python3 upload_pdf.py --ticket /absolute/path/to/private-ticket.json
```

The agent writes the ticket with permissions 600 and removes it afterwards. Never put it in Git or logs. The helper installs no runtime/daemon and scans no folders/attachments. If Python/picker is unavailable, use browser import or paper-page Upload.

Recent update: 2026-10-13 Standalone picker guide; browser import is the runtime-free starting path.
