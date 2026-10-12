---
name: prdb-setup
description: Set up a PRDB reading connection or diagnose missing PRDB tools and ordinary reading permissions. Use for this plugin's onboarding, not PRDB administration.
---

This is the **PRDB public trial**. The public package connects to
`https://prdb.ai/mcp`; use the address supplied by the installed package and check
the actual environment with `get_connection`. Developer packages may connect to
other environments, with separate accounts and grants. This trial is distributed
through `https://github.com/giorgioercixu/prdb-plugin`, not the reviewed OpenAI
directory. Do not edit a client's global configuration without permission.

1. If not installed, use the public repository's README for the current installation
   steps. With explicit user authorization and an available Codex CLI, add
   `giorgioercixu/prdb-plugin --ref v0.1.0` as a marketplace, then install
   `prdb@prdb`. Use the plugin UI when available; start a fresh conversation after
   installation. Do not install a server runtime or clone the PRDB application.
   If the user has no ordinary PRDB account, direct them to
   `https://prdb.ai/register` and let them complete email verification themselves.
   Check CLI availability before running it; if missing, provide the public guide
   and the client's HTTP MCP settings fallback rather than guessing an install command.
2. Let the client run OAuth in the browser. The user signs in with their ordinary
   PRDB account and chooses the permissions, expiry and private-data consent for their entire
   private Library, including future uploads; no paper selector is needed.
   Never ask for their PRDB password, OAuth access/refresh token, or admin credentials
   in chat. They can deselect requested permissions. New connections default to
   long-term access until revoked; 1, 7 or 30 days are optional. A null connection
   expires_at means no expiry, not an expired connection. OAuth access tokens still
   expire and refresh automatically; do not ask users to reconnect solely because
   an access token expired. Existing finite grants retain their expiry.
3. In a fresh conversation, call `get_connection`. Describe actual Library or legacy paper scope,
   expiry and permissions. If unavailable, report the failed step; do not fall back
   to database access or a different owner/grant.
4. For an existing PDF, use the reading skill. For a new PDF, prefer the reading
   skill's browser file-selection workflow when a local picker is unnecessary;
   it works without Python. For chat-side single-file handoff, explain the optional
   human file picker and browser approval. Folder access or
   a chat attachment does not automatically authorize an upload or identify its Paper.
   For export batches, explain the reading skill's browser folder selection and preview;
   this is not a third-party account scanner. Private note import requires notes:write.
   Public review requests require the optional reviews:publish permission and a separate
   owner confirmation for every exact body. Older grants do not gain these scopes.
5. Explain revocation in My Account → Connections. A password change also disables
   connections. Do not silently broaden a grant or publish a review.

Client installation, OAuth callback and actual attachment transport need separate
client tests. An HTTP SDK test alone is not a successful Codex Desktop installation.
