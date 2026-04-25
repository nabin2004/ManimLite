# Phase 006 — Draw a point

## Goal of this phase

Implement the smallest drawing operation: set one cell, with bounds checks.

## Problem being solved

Every higher-level primitive devolves to “write some cells.” If points are wrong, everything is wrong.

## Implementation

```python
from __future__ import annotations

WIDTH, HEIGHT = 32, 16
BG = " "


def blank_frame() -> list[list[str]]:
    return [[BG for _ in range(WIDTH)] for _ in range(HEIGHT)]


def set_pixel(frame: list[list[str]], x: int, y: int, ch: str = "#") -> None:
    if not (0 <= x < WIDTH and 0 <= y < HEIGHT):
        return
    frame[y][x] = ch[0]


def show(frame: list[list[str]]) -> None:
    for row in frame:
        print("".join(row))


if __name__ == "__main__":
    f = blank_frame()
    set_pixel(f, 5, 3)
    show(f)
```

## Explanation

We **clip** out-of-bounds writes instead of crashing—good for early experiments. In a real engine you may want debug assertions; here we favor “always show something.”

## Limitations

One character per pixel; no thickness; no anti-aliasing.

## Next phase preview

Phase 007 — Bresenham line drawing on the same grid.
