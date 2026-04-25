# Phase 035 — `Scale` animation

## Goal of this phase

Animate a **scale factor** (uniform) from `s0` to `s1` for objects that have `scale: float`.

## Problem being solved

Scale is a second lerp target alongside translation—same `t`, different channels.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Scalable:
    scale: float = 1.0


@dataclass
class Scale:
    s0: float
    s1: float

    def apply(self, o: Scalable, t: float) -> None:
        t = max(0.0, min(1.0, t))
        o.scale = self.s0 + (self.s1 - self.s0) * t


if __name__ == "__main__":
    o = Scalable(0.2)
    sc = Scale(0.2, 1.0)
    for t in (0, 0.5, 1.0):
        sc.apply(o, t)
        print(t, o.scale)
```

## Explanation

Non-uniform scale `(sx, sy)` is the same story with two lerps. Rotation later uses a different math path (transform composition).

## Limitations

Transform order (translate then scale vs the reverse) is not addressed until Phase 051+.

## Next phase preview

Phase 036 — Stacking `Move` + `Fade` on one object needs rules (order, exclusivity, or a timeline).
