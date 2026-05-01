# Typmotion roadmap

Milestones from the project proposal, adjusted for Kitten TTS voice-over and no Marp in core scope.

## v0.1 Alpha (weeks 1–8)

- Core renderer (Skia)
- Basic shapes
- MP4 output (PyAV)
- Scene + timeline stubs wired to a minimal render path

## v0.2 Alpha

- Full primitive set (shapes, text, code blocks)
- Math rendering (Typst → cached SVG)

## v0.3 Beta

- Animation system (fade, move, transform, easing, groups)
- Audio: background tracks + **Kitten TTS** narration + pydub mix + mux

## v0.4 Beta

- Templates (intro/outro, themes)
- Docker image for reproducible builds

## v0.9 RC

- PyPI release discipline (semver, changelog)
- Documentation site (MkDocs) + examples gallery

## v1.0 Stable

- Production-ready API stability guarantees
- Performance benchmarks vs ManimCE (documented methodology)

## Continuous

- CI: Ruff, mypy, pytest on Python 3.11 and 3.12
- ADRs for stack changes
- Requirements traceability in [SRS](requirements/SRS.md)
