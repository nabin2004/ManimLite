# Phase 023 — Color and stroke (data only)

## Goal of this phase

Add fields for **stroke color** and **width** on shapes—even if the ASCII backend ignores them. This is **data modeling** for the real engine.

## Problem being solved

If you add color after 5,000 lines, you will thread parameters everywhere. Early fields, late rendering.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Style:
    """RGBA 0..1 for teaching; real code may use 0..255 + separate alpha."""

    r: float = 1.0
    g: float = 1.0
    b: float = 1.0
    a: float = 1.0
    stroke_width: float = 1.0


@dataclass
class Circle:
    cx: float
    cy: float
    r: float
    style: Style = Style()
    ch: str = "o"  # ASCII debug glyph

    def draw(self, frame: list[list[str]]) -> None:
        # `style` is for Skia/NumPy later; ASCII: draw a single marker
        w, h = len(frame[0]), len(frame)
        x, y = int(self.cx), int(self.cy)
        if 0 <= x < w and 0 <= y < h:
            frame[y][x] = self.ch[0]
        _ = self.style  # kept so the object models real stroke/fill
```

## Explanation

**Separation of concerns:** geometry (cx, cy, r) vs appearance (`Style`). A Skia path stroke uses `stroke_width`; a fill would use a different `Paint` (later).

## Limitations

The toy ASCII renderer cannot show RGBA. This is intentional—don’t conflate *display* and *data*.

## Next phase preview

Phase 024 — Z-order: draw order in the list = painter’s algorithm (for now).
