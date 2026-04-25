# Phase 046 — Generic tween (careful)

## Goal of this phase

Sketch **tweening a named float attribute** with `getattr`/`setattr`—and show the footguns.

## Problem being solved

You want *one* animator type to move `x`, `y`, `opacity` without 30 classes. Generic tween is the shortest path, not the safest.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Obj:
    x: float
    y: float


@dataclass(frozen=True, slots=True)
class TweenFloat:
    name: str
    a: float
    b: float

    def apply(self, o: object, t: float) -> None:
        t = max(0.0, min(1.0, t))
        v = self.a + (self.b - self.a) * t
        setattr(o, self.name, v)


if __name__ == "__main__":
    p = Obj(0, 0)
    TweenFloat("x", 0, 10).apply(p, 0.5)
    print(p.x, p.y)
```

## Explanation

This is **stringly typed** and fails silently if the attribute name is wrong. Use it behind small helpers or keep explicit `MoveX` in public APIs for LLM success rates.

## Limitations

No path tweening (nested attrs), no units, no type checks.

## Next phase preview

Phase 047 — Property-level animation in a typed way: `Channel` enums or `dataclass` field descriptors.
