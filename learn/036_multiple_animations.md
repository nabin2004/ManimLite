# Phase 036 — Multiple animations on one node

## Goal of this phase

Show the **ordering** problem: `Move` then `Fade` vs `Fade` then `Move` can differ; if both run in parallel, results need a defined rule.

## Problem being solved

Without a timeline, ad hoc `apply` calls produce surprising combinations.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Obj:
    x: float
    y: float
    opacity: float


@dataclass
class Move:
    x0: float
    y0: float
    x1: float
    y1: float

    def apply(self, o: Obj, t: float) -> None:
        t = max(0.0, min(1.0, t))
        o.x = self.x0 + (self.x1 - self.x0) * t
        o.y = self.y0 + (self.y1 - self.y0) * t


@dataclass
class FadeTo:
    a0: float
    a1: float

    def apply(self, o: Obj, t: float) -> None:
        t = max(0.0, min(1.0, t))
        o.opacity = self.a0 + (self.a1 - self.a0) * t


# Rule example: at time t, run both with SAME t (parallel components)
# Alternative: run sequentially by splitting t — timeline fixes this
```

## Explanation

A **timeline** (Phase 037) is the user-visible fix: each channel has a schedule. Until then, keep rules explicit in code.

## Limitations

No graph solving for conflicting constraints—Typmotion stays explicit.

## Next phase preview

Phase 037 — `Timeline` of tuples `(t0, t1, target, animator)`.
