# PRDB · public trial

Read papers with your agent. Search PRDB, upload your own private PDFs, save exact highlights and comments, and keep private reviews in the Library you use on the website.

**Plugin 0.1.0 · Codex · https://prdb.ai/mcp.** Distributed through [prdb-plugin](https://github.com/giorgioercixu/prdb-plugin), not an OpenAI-reviewed directory listing. Fresh-machine testing is still in progress. The website's older 0.0.10 download is a separate preview; use this repository's version for the trial.

## 1. Create your account

[Register at prdb.ai](https://prdb.ai/register) and complete email verification. Use your own ordinary account. No demo account, administrator access or PRDB application source is needed.

## 2. Install in Codex Desktop

Open Codex Desktop and paste this into a chat:

> Install the PRDB public trial from https://github.com/giorgioercixu/prdb-plugin, pinned to v0.1.0. You may add this one marketplace and install prdb@prdb. Check that the Codex CLI supports plugin commands first, preserve my other settings, and do not copy credentials from another computer. Tell me when to start a new chat and authorize PRDB in my browser.

The supported CLI path, for you or your agent:

```sh
codex plugin marketplace add giorgioercixu/prdb-plugin --ref v0.1.0
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

For chat-side handoff, the optional packaged helper needs Python 3 and an OS picker. The agent requests an upload; you select a file in the picker and approve the actual file/Paper in your browser. Upload needs no copyright statement or password re-entry. A chat attachment is not automatically available to remote MCP: generic direct attachment transfer is not implemented. Record which path worked: browser import, native picker or website Upload.

Each PDF must be at most 30 MiB. Scanned/encrypted PDFs and absent catalog papers may need another workflow; the agent should report the limitation, not guess a paper or passage. Export batches support up to 50 PDFs/300 MiB; first finish the one-paper trial.

## 5. Highlight, comment and save a private review

> Read my uploaded PDF in PRDB. Find two exact passages relevant to its main contribution. Save private highlights with my comments, then save a private review draft referencing them. Check every source at the saved draft revision and give me Reader and private review links. Do not publish.

The agent uses actual PDF text and location candidates; ambiguous passages need clarification. Open Reader beside your chat and check the positions, comments and private review. Refresh and confirm the same content remains. Source checks validate text and versions, not scientific conclusions.

Public review publication is optional: the agent prepares a preview and you personally confirm the exact public body in the browser. Installing the plugin never publishes a private PDF or draft.

## Update, revoke or remove

- Read the next release notes before changing versions. The pinned v0.1.0 does not follow `main`. To switch to an approved newer tag, repeat `codex plugin marketplace add giorgioercixu/prdb-plugin --ref <new-tag>`, then refresh the marketplace/install according to the client. Start a new chat and check the actual installed version.
- Revoke in [My Account → Connections](https://prdb.ai/profile#connections). Local uninstall is not PRDB revocation. Your saved material remains available on the website.
- Uninstall: `codex plugin remove prdb@prdb`. Remove this marketplace too: `codex plugin marketplace remove prdb`.
- For an old `prdb-reading-preview`, explicitly disable/remove it and revoke its connection when no longer needed. Then install PRDB and authorize it anew. Old grants are not silently expanded.

## Feedback

Use [public installation/UX issues](https://github.com/giorgioercixu/prdb-plugin/issues/new/choose) for non-private reports, or [PRDB Support](https://prdb.ai/support) / issues@prdb.ai for private reports. Include OS, Codex version, plugin version, failing step, expected/actual result and a redacted error/screenshot. Never post passwords, tokens, private PDFs or notes publicly.

Try one paper, then two or three more; note the manual steps and time required. Fresh-machine human feedback is separate from parser/SDK/automated checks.

Recent update: 2026-10-13 PRDB 0.1.0 public-trial installation, OAuth, first PDF and feedback guide.
