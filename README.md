# PRDB

**Read papers with your agent.** Search PRDB, upload your own private PDFs, highlight exact passages, write comments and save private reviews beside the web Reader.

![PRDB](plugins/prdb/assets/icon.png)

**Public trial 0.1.0 for Codex Desktop.** Connects to [prdb.ai](https://prdb.ai). This repository contains only the plugin and optional file picker; no application server, accounts or private material. It has not been submitted to the OpenAI public directory.

## Start here

1. [Register and verify your ordinary PRDB account](https://prdb.ai/register).
2. Follow [the step-by-step quickstart](QUICKSTART.md) to install the pinned PRDB plugin and authorize it in your browser.
3. Upload one PDF, save highlights/comments/private review and check the same content in PRDB Reader.
4. [Report your experience](https://github.com/giorgioercixu/prdb-plugin/issues/new/choose); keep private material out of public issues.

Ask Codex:

> Install the PRDB public trial from https://github.com/giorgioercixu/prdb-plugin, pinned to v0.1.0. You may add this marketplace and install prdb@prdb, preserving other settings. Check the Codex CLI first, then tell me when to start a new chat and authorize PRDB in my browser.

For an available Codex CLI:

```sh
codex plugin marketplace add giorgioercixu/prdb-plugin --ref v0.1.0
codex plugin add prdb@prdb
```

## Downloads and status

[Release v0.1.0](https://github.com/giorgioercixu/prdb-plugin/releases/tag/v0.1.0) contains the Codex ZIP, SHA256SUMS and file manifest. Repository installation uses the same package at `plugins/prdb`. [Release notes](CHANGELOG.md) distinguish plugin versions from website releases.

Remote reading requires no local MCP server or Python package. A single PDF can be imported in your browser; the optional OS picker requires Python 3. Generic direct chat attachment transfer and other clients have not been accepted. Fresh-machine human testing is the purpose of this trial; automated parsing is not a human reading test.

## Repository contents

- [QUICKSTART](QUICKSTART.md): install, OAuth, upload, reading, update and removal.
- [plugins](plugins/README.md): PRDB manifest, production MCP connection, skills and icon.
- [.agents](.agents/README.md): installable Codex marketplace.
- [.github](.github/README.md): bug and trial feedback templates.
- [SECURITY](SECURITY.md): private reporting channel.
- [LICENSE-NOTICE](LICENSE-NOTICE.md): current distribution notice.

Use [PRDB Support](https://prdb.ai/support) or issues@prdb.ai for private reports. Do not include passwords, tokens, private PDFs or notes in public issues.

Recent update: 2026-10-13 Initial PRDB public trial; official directory review deferred until ordinary-user iterations are stable.
