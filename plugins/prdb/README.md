# PRDB · public trial

Read papers with your agent. Search PRDB, upload your own private PDFs, save exact highlights and comments, and keep private reviews in the Library you use on the website.

**Plugin 0.2.0 · Codex · https://prdb.ai/mcp.** Distributed through [prdb-plugin](https://github.com/giorgioercixu/prdb-plugin), not an OpenAI-reviewed directory listing. Fresh-machine testing is still in progress. Use the matching package for your environment; staging and production accounts are separate.

## 1. Create your account

[Register at prdb.ai](https://prdb.ai/register) and complete email verification. Use your own ordinary account. No demo account, administrator access or PRDB application source is needed.

## 2. Install in Codex Desktop

Open Codex Desktop and paste this into a chat:

> Install the PRDB public trial from https://github.com/giorgioercixu/prdb-plugin, pinned to v0.2.0. You may add this one marketplace and install prdb@prdb. Check that the Codex CLI supports plugin commands first, preserve my other settings, and do not copy credentials from another computer. Tell me when to start a new chat and authorize PRDB in my browser.

The supported CLI path, for you or your agent:

```sh
codex plugin marketplace add giorgioercixu/prdb-plugin --ref v0.2.0
codex plugin add prdb@prdb
```

Open Plugins, check that **PRDB** is enabled and start a **new chat**. If installation asks you to connect, follow step 3. If the commands are unavailable, update the client or report its version; do not hand-edit credential files.

No local MCP server, Python package or npm package is required for remote reading. Client versions and managed workspace restrictions can affect marketplace support. This trial targets Codex Desktop; ChatGPT web, Claude, Cursor and WorkBuddy have not been accepted for this package.

## 3. Connect your account

Run PRDB setup or ask:

> Use PRDB and check my reading connection. Help me connect through browser OAuth if necessary.

Sign in to PRDB in the browser and review the requested operations. New connections cover your **entire private Library**, including future uploads, and default to access until revoked; 1, 7 or 30 days are optional. Select the operations you want. Authorized private materials can be passed to your external agent. Complete identity confirmation in the browser; never paste passwords or tokens into chat.

Ask the agent to call `get_connection` and report the environment, permissions and expiry. It should report **production**, with your account. An enabled plugin alone does not prove tools loaded or authorization finished.

## 4. Upload your first PDF

Start with one PDF containing selectable text, for a paper in the PRDB catalog:

> Find [paper title] in PRDB and show its title, authors and year. Open a private import for one PDF so I can select the file and confirm its paper in the browser. After I upload, check the import result and read a page. Do not publish anything.

Open the returned browser link, select your PDF, review the match and approve the upload. This route needs **no Python**. The agent checks the uploaded document, rather than calling a pending preview a completed upload. The ordinary paper-page **Upload** button also works.

For a chat attachment or folder, explicitly give your agent access to the actual file or selected directory and ask it to upload privately. On POSIX systems, the optional Python 3 helper inspects only that granted root, rejects symlinks and path escapes, checks actual PDF bytes and SHA-256, and uploads through a short-lived lease. The agent matches the title/DOI/authors to the PRDB catalog and keeps a private progress journal for retries. It must leave ambiguous or absent catalog matches for you to resolve. A chat attachment works only if your client exposes a readable local file; that client path still needs real-user testing. Browser import and the OS picker remain available; no copyright declaration or password re-entry is required for uploading.
Each PDF must be at most 30 MiB. Scanned/encrypted PDFs and absent catalog papers may need another workflow; the agent should report the limitation, not guess a paper or passage. Export batches support up to 50 PDFs/300 MiB; first finish the one-paper trial.

## 5. Highlight, comment and save a private review

> Read my uploaded PDF in PRDB. Find two exact passages relevant to its main contribution. Save private highlights with my comments, then save a private review draft referencing them. Check every source at the saved draft revision and give me Reader and private review links. Do not publish.

The agent uses actual PDF text and location candidates; ambiguous passages need clarification. Open Reader beside your chat and check the positions, comments and private review. Refresh and confirm the same content remains. Source checks validate text and versions, not scientific conclusions.

Public review publication is optional: the agent prepares a preview and you personally confirm the exact public body in the browser. Installing the plugin never publishes a private PDF or draft.

## Update, revoke or remove

- Read the next release notes before changing versions. The pinned v0.2.0 does not follow `main`. To switch to an approved newer tag, repeat `codex plugin marketplace add giorgioercixu/prdb-plugin --ref <new-tag>`, then refresh the marketplace/install according to the client. Start a new chat and check the actual installed version.
- Revoke in [My Account → Connections](https://prdb.ai/profile#connections). Local uninstall is not PRDB revocation. Your saved material remains available on the website.
- Uninstall: `codex plugin remove prdb@prdb`. Remove this marketplace too: `codex plugin marketplace remove prdb`.
- For an old `prdb-reading-preview`, explicitly disable/remove it and revoke its connection when no longer needed. Then install PRDB and authorize it anew. Old grants are not silently expanded.

## Feedback

Use [public installation/UX issues](https://github.com/giorgioercixu/prdb-plugin/issues/new/choose) for non-private reports, or [PRDB Support](https://prdb.ai/support) / issues@prdb.ai for private reports. Include OS, Codex version, plugin version, failing step, expected/actual result and a redacted error/screenshot. Never post passwords, tokens, private PDFs or notes publicly.

Try one paper, then two or three more; note the manual steps and time required. Fresh-machine human feedback is separate from parser/SDK/automated checks.

## Library and daily actions

Choose the optional operation permissions in browser OAuth, then ask your agent to manage bookmarks, reading status, ratings, follows, discussions, notifications or your own profile/claims/support requests. Old connections do not gain new permissions automatically. Administrators decide claims independently; this plugin has no reviewer access. Public writes and deletion follow your explicit request.

Page images and long-page continuation complement text reading. Images do not provide OCR or accurate highlight coordinates by themselves. Public reviews still use PRDB's owner-confirmed browser preview; the experimental native chat confirmation is disabled until actual client verification.

Recent update: 2026-10-13 PRDB 0.2.0 release batch; three skills, optional operation permissions and granted-file transfers. Fresh-machine human acceptance remains pending.
