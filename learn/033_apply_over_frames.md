# Phase 033 — Apply over frames

## Goal of this phase

Drive `Move.apply` for **i = 0..N-1** with `t = i / (N-1)` to simulate a 1-second clip if `N = fps * duration`.

## Problem being solved

The wall clock and frame index are the bridge between *animation math* and *discrete video*.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Movable:
    x: float
    y: float


@dataclass
class Move:
    x0: float
    y0: float
    x1: float
    y1: float

    def apply(self, m: Movable, t: float) -> None:
        t = max(0.0, min(1.0, t))
        m.x = self.x0 + (self.x1 - self.x0) * t
        m.y = self.y0 + (self.y1 - self.y0) * t


def frame_times(n: int) -> list[float]:
    if n < 2:
        return [0.0] * max(0, n)
    return [i / (n - 1) for i in range(n)]


if __name__ == "__main__":
    m = Movable(0, 0)
    mv = Move(0, 0, 9, 0)
    for t in frame_times(5):
        mv.apply(m, t)
        print(f"{t:.2f} -> {m.x:.1f}, {m.y:.1f}")
```

## Explanation

The mapping `i -> t` is *uniform* here. If you use **easing** (Phase 040), you replace `t` with `eased(t)`.

## Limitations

Assumes all clips use the same ease-in time domain; out-of-order animation needs a `Scene` clock (Phase 037+).

## Next phase preview

Phase 034 — `Fade` = animate opacity `a` in `[0,1]`.
