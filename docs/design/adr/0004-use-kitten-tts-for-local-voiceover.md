# ADR-0004: Use Kitten TTS as the default local voice-over backend

- **Status:** Accepted (supersedes Piper / `piper-tts`)
- **Date:** 2026-04-25

## Context

Teaching workflows need optional **local** narration without cloud APIs. Piper (`piper-tts`) was initially chosen but is **GPL-3.0-or-later**, which complicates an otherwise MIT core.

## Decision

Adopt **[Kitten TTS](https://github.com/KittenML/KittenTTS)** as the default `VoiceOverBackend` implementation (`KittenVoiceOverBackend`), shipped only via the optional **`[tts]`** extra.

- Install: `uv sync --extra tts` (pulls the upstream **0.8.1** wheel URL plus `soundfile` for in-memory WAV).
- Default model: **`KittenML/kitten-tts-nano-0.8-int8`** (~25 MB on disk) with built-in voices such as **Jasper**, **Luna**, etc.

## Consequences

- **Positive:** **Apache-2.0** aligns better with the MIT core than GPL Piper; small CPU-friendly ONNX models; Hugging Face Hub caching.
- **Negative:** Kitten TTS is **developer preview** — APIs may change; first run may download model weights from the network. Current **0.8.1** wheels also resolve **heavy** transitive packages (e.g. **PyTorch**, **spaCy**) — far larger than the “~25–80 MB model” alone; revisit pins or upstream slimming in a future release.
- **Follow-up:** Pin wheel URL / versions in releases; document HF offline/cache layout; optional GPU backend (`backend="cuda"`) out of scope until needed.
