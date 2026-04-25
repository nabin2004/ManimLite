# Phase 051 — `Transform` dataclass

## Goal of this phase

Unify **translation + uniform scale** in one `@dataclass` you can lerp and compose later.

## Problem being solved

Separate `x,y` and `scale` without rules yields ambiguous order: translate then scale vs scale then translate.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Transform:
    x: float = 0.0
    y: float = 0.0
    sx: float = 1.0
    sy: float = 1.0

    def apply_point(self, px: float, py: float) -> tuple[float, float]:
        return (self.x + self.sx * px, self.y + self.sy * py)
```

## Explanation

This is the 2D **affine-ish** subset (no rotation yet). Order is: scale around origin, then translate (you can change convention, but **be consistent**).

## Limitations

Rotation and shear need a 2×3 matrix; Phase 053 hints at composition.

## Next phase preview

Phase 052 — Replace raw `cx,cy` on shapes with `Transform` + local geometry.
