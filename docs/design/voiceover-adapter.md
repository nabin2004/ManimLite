# Voice-over adapter (Kitten TTS)

## Goals

- **Local-first** teaching narration (no cloud TTS API)
- **Apache-2.0** default engine ([Kitten TTS](https://github.com/KittenML/KittenTTS)) compatible with the MIT core
- **Pluggable** `VoiceOverBackend` for future engines
- **Timeline-aligned** audio muxed with MP4

## Default backend: Kitten TTS

- Python package: **`kittentts`** (installed from the upstream **0.8.1** wheel URL via optional extra `[tts]`; see [pyproject.toml](../../pyproject.toml)).
- **Footprint:** upstream currently pulls a **large** stack (e.g. PyTorch-related wheels) in addition to the ONNX weights — the `[tts]` extra is intentionally **not** part of the lean core install.
- **License:** Apache-2.0 (per upstream).
- Models are pulled from **Hugging Face Hub** (e.g. `KittenML/kitten-tts-nano-0.8-int8`, ~25 MB int8) into the default HF cache unless `cache_dir` is set on the backend (future).
- **Voices:** built-in names such as `Jasper`, `Luna`, `Bella`, … (see upstream `available_voices`).
- **Output:** 24 kHz samples; Typmotion wraps synthesis as **in-memory WAV** via `soundfile` for pydub / PyAV.

## Public API (sketch)

```python
from typmotion import Scene, VoiceOver, KittenVoiceOverBackend

scene = Scene()
vo = VoiceOver(
    text="This high-quality TTS model runs without a GPU.",
    voice="Jasper",
    start=0.0,
)
scene.narrate(vo)
bytes_wav = vo.synthesize(KittenVoiceOverBackend())
```

Use `KittenVoiceOverBackend(model_name="KittenML/kitten-tts-mini-0.8", speed=1.0, clean_text=True)` to match upstream defaults for quality / preprocessing.

## Pipeline

1. **Collect** all `VoiceOver` instances from the scene (order + start time).
2. **Synthesize** each clip via `VoiceOverBackend.synthesize` → WAV bytes (Kitten path: `KittenTTS.generate` → `soundfile` → `BytesIO`).
3. **Place** segments on a master timeline (start offsets).
4. **Mix** optional background music with **pydub**.
5. **Mux** final audio with video in PyAV (resample if needed).

## Timeline alignment

- **Mode A (explicit):** user sets `Scene.duration` ≥ narration end.
- **Mode B (auto-extend, optional flag):** extend scene duration if narration exceeds `duration` (ADR when implemented).

## Extension point

```python
class VoiceOverBackend(Protocol):
    def synthesize(self, text: str, *, voice: str) -> bytes: ...
```

Non-Kitten backends (cloud or other local engines) implement the same protocol without changing `VoiceOver` fields.

## Security / privacy

- **Network:** first model load may hit Hugging Face Hub unless models are pre-seeded in cache.
- **Cache:** align with upstream / HF cache conventions; document offline mirroring for air-gapped builds.

## Testing strategy

- **Unit:** mock backend returns fixed WAV bytes; mixer places samples correctly.
- **Integration (optional):** with `[tts]` installed, one short `generate` smoke test (may download weights — mark slow or run locally only).

## Related

- [ADR-0004](adr/0004-use-kitten-tts-for-local-voiceover.md)
- [SRS.md](../requirements/SRS.md) FR-13–FR-15
