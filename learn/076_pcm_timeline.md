# Phase 076 — PCM timeline

## Goal of this phase

Represent **audio events** as `(t0, samples)` on the same clock as video `T`.

## Problem being solved

If audio and video are computed with different time bases, **muxing** is painful.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AudioEvent:
    t0: float
    # conceptual: int16 mono PCM at 48_000 Hz
    # samples: memoryview
```

## Explanation

A real library stores `ndarray` int16, sample rate, channel count, and layout. Resampling to the encoder’s rate happens once.

## Limitations

No loudness / limiter; educational scope.

## Next phase preview

Phase 077 — **Muxing** A+V with PyAV: interleaving, clock drift.
