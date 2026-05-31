# Phase 067 — Time-driven loop

## Goal of this phase

Connect **real seconds** to frame index: `T = i / fps` for a CFR export or `T = cumsum(deltas)`.

## Problem being solved

If time drifts, audio desyncs. CFR (constant frame rate) is the simplest first policy.

## Implementation

```python
from __future__ import annotations


def frame_times_cfr(n: int, duration: float) -> list[float]:
    if n <= 0:
        return []
    if n == 1:
        return [0.0]
    return [duration * (i / (n - 1)) for i in range(n)]
```

## Explanation

MotionGram should pick one time mapping and test it. Constant **Δt = 1/fps** is another common form; both work if **consistent** with the encoder’s `time_base`.

## Limitations

For variable fps content, you need per-frame duration metadata—out of initial scope.

## Next phase preview

Phase 068 — The `Scene.save` user-facing function signature.
