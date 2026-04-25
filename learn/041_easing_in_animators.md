# Phase 041 — Easing in animators

## Goal of this phase

Pass an **easing function** into `apply` (or pre-wrap `t`) so the same `Move` can feel different.

## Problem being solved

Copy/pasting `Move` for each easing is worse than a parameter.

## Implementation

```python
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

Easer = Callable[[float], float]


def ease_in_out_quad(t: float) -> float:
    t = max(0.0, min(1.0, t))
    if t < 0.5:
        return 2 * t * t
    return 1 - ((-2 * t + 2) ** 2) / 2


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

    def apply(self, m: Movable, t: float, ease: Easer = lambda u: u) -> None:
        u = max(0.0, min(1.0, t))
        u = ease(u)
        m.x = self.x0 + (self.x1 - self.x0) * u
        m.y = self.y0 + (self.y1 - self.y0) * u


if __name__ == "__main__":
    m1 = Movable(0, 0)
    m2 = Movable(0, 0)
    mv = Move(0, 0, 10, 0)
    mv.apply(m1, 0.5, ease_in_out_quad)
    mv.apply(m2, 0.5, lambda u: u)
    print(m1.x, m2.x)
```

## Explanation

Easing is **orthogonal** to the geometric meaning of the animator.

## Limitations

Overshoot/bounce eases can produce values >1 in naive lerps; clamp carefully per channel if needed.

## Next phase preview

Phase 042 — A **dispatcher** that, given global time `T`, finds active entries and local `t`.
