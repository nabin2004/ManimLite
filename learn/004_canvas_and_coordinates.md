# Phase 004 — Canvas and coordinates

## Goal of this phase

Fix a single coordinate convention so every drawing function matches your mental model.

## Problem being solved

If `x` increases downward in one function and upward in another, debugging becomes guesswork.

## Implementation

We adopt a **top-left origin** like image pixels: `x` increases right, `y` increases **down**.

```python
from __future__ import annotations

WIDTH, HEIGHT = 16, 8


def in_bounds(x: int, y: int) -> bool:
    return 0 <= x < WIDTH and 0 <= y < HEIGHT
```

## Explanation

Raster APIs (and numpy image arrays) commonly use top-left origins. If you later flip `y` for “math coordinates,” do it **once** at a boundary (camera), not inside every primitive.

## Limitations

Integer pixel centers only here; subpixel antialiasing waits for a real renderer (Phase 028+).

## Next phase preview

Phase 005 — A print-based “framebuffer” as a 2D list of characters.
