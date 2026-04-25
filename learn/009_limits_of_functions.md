# Phase 009 — Limits of functions

## Goal of this phase

Hit the wall on purpose: **global parameters**, **tangled function signatures**, and **no place for state** that belongs together.

## Problem being solved

Functions + loose globals work for 50 lines, then they rot. This phase names the smells you will fix with a `Node` in Phase 010.

## Implementation

This “program” draws two circles—already awkward.

```python
from __future__ import annotations

import math

WIDTH, HEIGHT = 32, 16
BG = " "


def blank() -> list[list[str]]:
    return [[BG for _ in range(WIDTH)] for _ in range(HEIGHT)]


def setp(f: list[list[str]], x: int, y: int, ch: str) -> None:
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        f[y][x] = ch[0]


def circle(f: list[list[str]], cx: int, cy: int, r: int, ch: str) -> None:
    n = max(8, r * 8)
    for i in range(n):
        t = 2 * math.pi * i / n
        x = int(round(cx + r * math.cos(t)))
        y = int(round(cy + r * math.sin(t)))
        setp(f, x, y, ch)


def show(f: list[list[str]]) -> None:
    for row in f:
        print("".join(row))


if __name__ == "__main__":
    f = blank()
    circle(f, 10, 8, 4, "A")
    circle(f, 20, 8, 4, "B")  # which circle is "which" in the data model? nowhere.
    show(f)
```

## Explanation

You can keep threading `f` (frame) everywhere, but the **object you care about** is “a circle at (10,8) with r=4.” That bundle wants a home—**state + behavior** in one place.

## Limitations

No animation yet; no scene; no z-order (depends on call order of drawing). Next phase gives the minimal class.

## Next phase preview

Phase 010 — `Node` class: one drawable object with a position you can name.
