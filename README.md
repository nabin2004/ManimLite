# ManimLite

**Unofficial lightweight animation engine** — inspired by [Manim Community Edition](https://www.manim.community/), built for **speed** and **LLM-friendly** code generation.

| Goal | Target |
|------|--------|
| Cold render | ~10× faster than typical ManimCE disk+LaTeX pipelines |
| Install size | ~80 MB core (`[tts]` optional: upstream Kitten stack + HF models, much larger) |
| Math | Typst → SVG (no TeX Live) |
| Render | Skia (no Cairo) |
| Encode | PyAV in-memory (no per-frame disk + FFmpeg subprocess) |
| Voice-over | [Kitten TTS](https://github.com/KittenML/KittenTTS) local TTS, Apache-2.0 (optional `[tts]` extra) |

Installing `[tts]` may pull a **large** dependency tree (for example **PyTorch** and friends) as required by upstream **kittentts** 0.8.x — keep it optional. Core animation deps stay separate.

**Status:** pre-alpha — core rendering pipeline (Skia + Typst + PyAV) is functional; see [docs/](docs/) for requirements and design.

**Tutorial:** step-by-step build from ASCII to PyAV-oriented design in [learn/](learn/) (phases `000`–`100`).

## Quick start

```bash
# Install (requires Python 3.11+)
uv pip install -e ".[dev]"

# Install Typst CLI for math rendering
curl -fsSL https://github.com/typst/typst/releases/latest/download/typst-x86_64-unknown-linux-musl.tar.xz \
  | tar -xJ --strip-components=1 -C ~/.local/bin/

# Polished 720p showcase (recommended)
manimlite render examples/showcase_intro.py -o showcase.mp4

# Full-stack demo (text + math + code + circle)
manimlite render examples/math_and_text.py -o output.mp4

# Or run directly
python examples/showcase_intro.py
python examples/math_and_text.py
```

See the [Setup Guide](docs/guides/setup.md) for platform-specific instructions.

## Documentation

- [Setup Guide](docs/guides/setup.md) — installing skia-python and Typst
- [Math Rendering Guide](docs/guides/math-rendering.md) — using Typst for math
- [Learn path (phases 000–100)](learn/README.md)
- [Proposal](docs/proposal.md)
- [Roadmap](docs/roadmap.md)
- [Software Requirements Specification (SRS)](docs/requirements/SRS.md)
- [Software Design Document (SDD)](docs/design/SDD.md)
- [Architecture](docs/design/architecture.md)

## License

MIT — see [LICENSE](LICENSE).

## Author

Nabin Oli
