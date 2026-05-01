# Phase 049 — `N` frames

## Goal of this phase

Discretize **continuous time** into frame indices: `N = round(duration * fps)`.

## Problem being solved

Video is a finite set of instants. You need a policy for inclusive/exclusive ends.

## Implementation

```python
from __future__ import annotations

import math


def frame_count(duration_s: float, fps: float) -> int:
    if duration_s <= 0 or fps <= 0:
        return 0
    return max(1, int(math.ceil(duration_s * fps)))


def frame_time(i: int, n: int, duration_s: float) -> float:
    """Map frame index i in [0, n-1] to T in [0, duration_s]."""
    if n <= 1:
        return 0.0
    return duration_s * (i / (n - 1))


if __name__ == "__main__":
    d, fps = 1.0, 30
    n = int(d * fps)  # simple policy: 30 frames for 1s @30Hz
    print(n, [round(frame_time(i, n, d), 4) for i in (0, n // 2, n - 1)])
```

## Explanation

Off-by-one is the #1 video bug. Typmotion should document its chosen mapping (ceil vs floor) in one place; here we just illustrate the *need* for a spec.

## Limitations

No alignment to sample grid for audio; Phase 077 touches mux alignment.

## Next phase preview

Phase 050 — **Video** as an iterator of in-memory frames—no `ffmpeg` CLI, no PNG sequences.
