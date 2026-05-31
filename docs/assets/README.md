# Static assets

Small media checked into git for documentation (for example the README demo reel).

- **`readme-demo.mp4`** — short showcase rendered from `examples/showcase_intro.py`. Safe to replace after improving the example; keep file size modest so clones stay fast.

All other `*.mp4` outputs (CLI renders, `examples/principles/*.mp4`, etc.) remain ignored by `.gitignore`.

Regenerate:

```bash
motiongram render examples/showcase_intro.py -o docs/assets/readme-demo.mp4
```
