# Phase 053 — Compose transforms

## Goal of this phase

Define `parent * child` for translate+scale in a **consistent order** (documented).

## Problem being solved

Scene graphs only work if you know how local points map to world space.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class XF:
    x: float = 0.0
    y: float = 0.0
    s: float = 1.0


def compose(outer: XF, inner: XF) -> XF:
    # inner acts first, then outer (typical: local -> parent)
    return XF(
        x=outer.x + outer.s * inner.x,
        y=outer.y + outer.s * inner.y,
        s=outer.s * inner.s,
    )


if __name__ == "__main__":
    world = compose(XF(10, 0, 2), XF(5, 0, 1))
    print(world)
```

## Explanation

This is a tiny subset of 2D affine composition. A full 3×3 matrix (homogeneous coords) is the scalable path for rotation.

## Limitations

Non-commutative; order bugs look like “my group jumped sideways.”

## Next phase preview

Phase 054 — Each `Node` stores `transform`; parent world transform is a fold over the path.
