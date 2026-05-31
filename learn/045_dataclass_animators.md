# Phase 045 — Dataclass animators

## Goal of this phase

Use `@dataclass` animators (frozen where possible) with an `apply(target, t)` for **type clarity** and **repr**.

## Problem being solved

Closures are great, but a dataclass is easier to log, store, and test.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Obj:
    x: float


@dataclass(frozen=True, slots=True)
class MoveX:
    x0: float
    x1: float

    def apply(self, o: Obj, t: float) -> None:
        t = max(0.0, min(1.0, t))
        o.x = self.x0 + (self.x1 - self.x0) * t
```

## Explanation

`MoveX` is a **value object**; `Obj` is the mutable world state. This separation maps cleanly to MotionGram’s public API.

## Limitations

You still need a way to *route* the animator to the right object field—see generic tweening next.

## Next phase preview

Phase 046 — A generic **attribute tween** (by name) with caution.
