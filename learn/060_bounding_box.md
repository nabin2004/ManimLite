# Phase 060 — Bounding box

## Goal of this phase

Compute an **axis-aligned bounding box (AABB)** in world space for a circle and a line—simple, fast, and good enough for layout.

## Problem being solved

Camera fitting, culling, and “is this on screen” need extents, not per-pixel tests.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BBox:
    x0: float
    y0: float
    x1: float
    y1: float


@dataclass
class XF:
    x: float
    y: float
    s: float = 1.0


def circle_aabb(cx: float, cy: float, r: float) -> BBox:
    return BBox(cx - r, cy - r, cx + r, cy + r)


def xform_aabb(b: BBox, xf: XF) -> BBox:
    # conservative for translation + uniform scale (corners)
    return BBox(
        xf.x + xf.s * b.x0,
        xf.y + xf.s * b.y0,
        xf.x + xf.s * b.x1,
        xf.y + xf.s * b.y1,
    )
```

## Explanation

For rotated shapes, AABB in world space **grows** (looser). Use an oriented box or a convex hull when rotation matters.

## Limitations

No stroke width inflation—real stroking widens bounds.

## Next phase preview

Phase 061 — **Dirty flags**: skip subtree redraw when not changed (concept).
