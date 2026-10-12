# PRDB plugin icon

`icon.svg` is the editable source; `icon.png` is its 512 × 512 PNG rendering used by Codex's plugin listing and composer. The paper symbol uses PRDB's Solarized blue and cream. Both ship with the plugin.

Maintainers regenerate the PNG with `ops/reading/render_icon.mjs` from the application workspace, using an available Sharp package. The optional argument points to that package's directory:

```sh
node ops/reading/render_icon.mjs /absolute/path/to/node_modules/sharp
```

Users do not need Node or Sharp to install this plugin.

Recent update: 2026-10-13 Added the shared PRDB trial icon and its reproducible rendering source.
