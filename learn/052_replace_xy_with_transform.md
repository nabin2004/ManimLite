# Phase 052 — Replace raw `x, y` with `Transform`

## Goal of this phase

Store **local** geometry (unit circle) and a world `Transform`, not two coordinate systems mixed ad hoc.

## Problem being solved

When you animate position and scale independently, you want a single place to lerp.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Transform:
    x: float = 0.0
    y: float = 0.0
    s: float = 1.0


@dataclass
class CircleLocal:
    """Unit circle idea: radius in local space is 1; world scale controls size."""

    r: float = 1.0

    def world_radius(self, xf: Transform) -> float:
        return self.r * xf.s


@dataclass
class Circle:
    xf: Transform = Transform()
    r: float = 30.0
```

## Explanation

This is the same data as before, just **grouped**. The win is composition: `Group` can hold a `Transform` for all children.

## Limitations

Still no rotation; `r` duplicates if you also scale—pick one source of truth in your engine.

## Next phase preview

Phase 053 — Composing parent and child transforms.
