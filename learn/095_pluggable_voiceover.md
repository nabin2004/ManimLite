# Phase 095 — Pluggable voice-over

## Goal of this phase

Keep **`VoiceOverBackend`** as the seam: TTS, recorded WAV, or cloud APIs behind the same `synthesize()` contract.

## Problem being solved

Narration is a product feature with wildly different cost/latency/privacy. Hard-coding one engine in `Scene` is a mistake.

## Implementation

```python
class VoiceOverBackend(Protocol):
    def synthesize(self, text: str, *, voice: str) -> bytes: ...
```

## Explanation

The **timeline** only needs PCM/WAV or float samples at a **sample rate**; everything else is adapter code.

## Limitations

Cloud backends need API key management—never part of the core public defaults.

## Next phase preview

Phase 096 — **CI** recap: ruff, mypy, pytest tiers; optional slow jobs for PyAV/encoder.
