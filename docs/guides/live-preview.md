# Live YAML Preview

Edit a YAML manifest and see the rendered scene update beside your editor — similar to Markdown preview in VS Code or Cursor.

## Prerequisites

Same as the [Setup Guide](setup.md):

- Python 3.11+ with MotionGram installed (`uv pip install -e ".[dev]"`)
- Typst CLI on `PATH` (for math elements)
- skia-python working on your platform

## Quick start (terminal + browser)

From the repo root:

```bash
motiongram preview examples/yaml/deeplearning_showcase.yaml --video-on-save
```

You should see:

```
Preview server ready: http://127.0.0.1:8765
Watching: examples/yaml/deeplearning_showcase.yaml
```

Open **http://127.0.0.1:8765** in any browser. Edit the YAML file and save — the frame preview updates immediately. With `--video-on-save`, a full MP4 is encoded in the background (debounced ~2s after the last save) and appears in the video player when ready.

### CLI options

| Flag | Default | Description |
|------|---------|-------------|
| `--port` | `8765` | HTTP port |
| `--host` | `127.0.0.1` | Bind address |
| `--time` | `0s` | Initial scrub time on the timeline |
| `--video-on-save` | off | Background full MP4 encode after each save |

Example — start scrubbing at 4 seconds:

```bash
motiongram preview examples/yaml/deeplearning_showcase.yaml --time 4s
```

## VS Code / Cursor side-by-side

1. Open a `.yaml` manifest (e.g. `examples/yaml/deeplearning_showcase.yaml`).
2. **Terminal → Run Task…** (or `Ctrl+Shift+P` → *Tasks: Run Task*).
3. Choose **MotionGram: Preview YAML (side by side)**.
   - Starts the preview server in a dedicated terminal panel.
   - Opens the built-in **Simple Browser** at `http://127.0.0.1:8765`.
4. Drag the Simple Browser tab into the right editor group, or use **View → Editor Layout → Two Columns**.
5. Edit the YAML and save (`Ctrl+S`). The preview reloads on save.

### Individual tasks

| Task | What it does |
|------|----------------|
| **MotionGram: Live Preview** | Start the preview server only (with `--video-on-save`) |
| **MotionGram: Open Preview Browser** | Open Simple Browser to the preview URL |
| **MotionGram: Preview YAML (side by side)** | Both, in sequence |

No extra extensions are required — Simple Browser is built into VS Code and Cursor.

## Preview UI

- **Frame image** — single frame at the current scrub time; updates instantly on save.
- **Timeline scrubber** — drag to inspect any point in the animation without re-encoding.
- **Play frames** — client-side playback by fetching frames along the timeline.
- **Background video** — when `--video-on-save` is enabled, shows the latest encoded MP4 below the frame preview.
- **Error banner** — YAML validation errors are shown without stopping the server; the last good frame stays visible if one was rendered.

Preview artifacts are written to `.motiongram/preview.mp4` next to your manifest (gitignored).

## Workflow tips

- Use the scrubber to check layout and animation timing while editing element positions or durations.
- Invalid YAML during editing is normal — fix the error and save again; the banner clears on the next successful reload.
- For final output, use `motiongram render` as usual; preview MP4s use a fast encode preset and live in `.motiongram/`.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Address already in use` | Another preview server is running, or change `--port` |
| Blank frame / math missing | Ensure `typst` is on `PATH` (see [Setup Guide](setup.md)) |
| Simple Browser does not open | Run **MotionGram: Open Preview Browser** manually after the server starts |
| Video never appears | Pass `--video-on-save`; wait a few seconds after save for the background encode |
| `preview only supports .yaml` | Live preview is YAML-only in v1; use `motiongram render` for `.py` scenes |

## See also

- [YAML schema (SCHEMA.md)](../SCHEMA.md)
- [Setup Guide](setup.md)
