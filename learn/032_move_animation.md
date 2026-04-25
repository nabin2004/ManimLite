# Phase 032 — `Move` animation class

## Goal of this phase

The smallest animation object: **move a point** from A to B over `t in [0,1]`.

## Problem being solved

We need a concrete `Animation` that is not tied to a renderer yet—math only.

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

    def apply(self, target: Movable, t: float) -> None:
        t = max(0.0, min(1.0, t))
        target.x = self.x0 + (self.x1 - self.x0) * t
        target.y = self.y0 + (self.y1 - self.y0) * t


if __name__ == "__main__":
    m = Movable(0, 0)
    mv = Move(0, 0, 10, 5)
    for k in range(5):
        t = k / 4
        mv.apply(m, t)
        print(f"t={t:.2f} -> ({m.x:.2f}, {m.y:.2f})")
```

## Explanation

`apply(target, t)` is the *animator* pattern: **idempotent** if you re-run at same `t`, **deterministic** for the same parameters.

## Limitations

No scene clock yet—you drive `t` by hand. Phase 033 connects to frames.

## Next phase preview

Phase 033 — For `N` frames, sample `t = i / (N-1)` to produce a motion path.
