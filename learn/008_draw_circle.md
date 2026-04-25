# Phase 008 — Draw a circle

## Goal of this phase

Rasterize a **circle outline** (integer grid) to show that curves are still just pixels.

## Problem being solved

If you only have lines, everything curved becomes a polyline later. A circle is a first taste of “implicit shape → samples.”

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


def circle_outline(frame: list[list[str]], cx: int, cy: int, r: int, ch: str = "o") -> None:
    """Rasterize a circle by sampling (stdlib only). Intuitive; not fastest."""
    import math

    n = max(8, r * 8)
    for i in range(n):
        t = 2 * math.pi * i / n
        x = int(round(cx + r * math.cos(t)))
        y = int(round(cy + r * math.sin(t)))
        set_pixel(frame, x, y, ch)


def show(frame: list[list[str]]) -> None:
    for row in frame:
        print("".join(row))


if __name__ == "__main__":
    f = blank_frame()
    circle_outline(f, 16, 8, 6)
    show(f)
```

## Explanation

Symmetry is the trick: compute one arc, mirror to eight octants. Real engines also exploit symmetry, just with more math and AA.

## Limitations

Only outlines; not filled; integer radius; breaks if `r` is huge vs canvas.

## Next phase preview

Phase 009 — The wall: when functions and loose parameters don’t scale.
