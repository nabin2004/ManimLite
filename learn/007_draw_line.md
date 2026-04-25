# Phase 007 — Draw a line

## Goal of this phase

Draw a line segment on the ASCII grid using **integer** line rasterization (Bresenham).

## Problem being solved

Lines are the backbone of UI, axes, arrows, and polygon edges. Implementing Bresenham once teaches you how “vector” ideas become pixels.

## Implementation

```python
from __future__ import annotations

WIDTH, HEIGHT = 32, 16
BG = " "


def blank_frame() -> list[list[str]]:
    return [[BG for _ in range(WIDTH)] for _ in range(HEIGHT)]


def set_pixel(frame: list[list[str]], x: int, y: int, ch: str = "#") -> None:
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        frame[y][x] = ch[0]


def line(frame: list[list[str]], x0: int, y0: int, x1: int, y1: int, ch: str = "#") -> None:
    """Bresenham line (integer grid, all octants)."""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    x, y = x0, y0
    while True:
        set_pixel(frame, x, y, ch)
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy


def show(frame: list[list[str]]) -> None:
    for row in frame:
        print("".join(row))


if __name__ == "__main__":
    f = blank_frame()
    line(f, 2, 2, 28, 12, "*")
    show(f)
```

## Explanation

Bresenham visits each pixel on the best discrete approximation of a line. This is the same class of work a GPU does—just 10⁶ times faster.

## Limitations

No width; jagged diagonals; no correct handling of “too steep” for half-open line conventions beyond basic form.

## Next phase preview

Phase 008 — A circle (outline) with a midpoint integer algorithm.
