# Phase 078 — Voice-over hook

## Goal of this phase

Define a minimal API: `VoiceOver(text, start, voice_id)` and a `VoiceOverBackend` protocol (no cloud required).

## Problem being solved

Narration is a separate data stream: it must be **pluggable** (local TTS, baked WAV, cloud later) without forking the video pipeline.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class VoiceOver:
    text: str
    t0: float
    voice: str


class VoiceOverBackend(Protocol):
    def synthesize(self, text: str, *, voice: str) -> bytes: ...  # wav bytes, for example
```

## Explanation

The scene collects `VoiceOver` events; a mixer (Phase 080) lines them on the global clock; the exporter interleaves.

## Limitations

SSML, emphasis, and phoneme control are not in scope.

## Next phase preview

Phase 079 — **Kitten TTS** as one optional local backend (Apache-2.0; heavy upstream deps off-core).
