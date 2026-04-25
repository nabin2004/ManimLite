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

**Status:** pre-alpha — API and internals are stubs; see [docs/](docs/) for requirements and design.

## Quick start (placeholder)

```bash
uv sync --extra dev --extra tts
manimlite render examples/hello_circle.py
```

Implementation of `render` and the pipeline is tracked in the roadmap.

## Documentation

- [Proposal](docs/proposal.md)
- [Roadmap](docs/roadmap.md)
- [Software Requirements Specification (SRS)](docs/requirements/SRS.md)
- [Software Design Document (SDD)](docs/design/SDD.md)
- [Architecture](docs/design/architecture.md)

## License

MIT — see [LICENSE](LICENSE).

## Author

Nabin Oli
