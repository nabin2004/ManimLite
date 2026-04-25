# Phase 012 — Node position and shape parameters

## Goal of this phase

Show that a drawable object carries **all parameters** it needs, not just `(x, y)`.

## Problem being solved

If you hardcode size in the draw routine, you cannot animate scale later. We practice “attributes live on the object.”

## Implementation

We embed a small circle routine inside a `Disc` node. Still ASCII sampling.

```python
from __future__ import annotations

import math
from dataclasses import dataclass

WIDTH, HEIGHT = 40, 14
BG = " "


def blank() -> list[list[str]]:
    return [[BG for _ in range(WIDTH)] for _ in range(HEIGHT)]


def setp(f: list[list[str]], x: int, y: int, ch: str) -> None:
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        f[y][x] = ch[0]


@dataclass
class Disc:
    cx: int
    cy: int
    r: int
    ch: str = "o"

    def draw(self, frame: list[list[str]]) -> None:
        n = max(8, self.r * 8)
        for i in range(n):
            t = 2 * math.pi * i / n
            x = int(round(self.cx + self.r * math.cos(t)))
            y = int(round(self.cy + self.r * math.sin(t)))
            setp(frame, x, y, self.ch)


def show(f: list[list[str]]) -> None:
    for row in f:
        print("".join(row))


if __name__ == "__main__":
    f = blank()
    Disc(12, 7, 4, "A").draw(f)
    Disc(28, 7, 3, "B").draw(f)  # second draws on top where pixels overlap
    show(f)
```

## Explanation

`Disc` is your first *real* “shape” object. Position is `(cx, cy)`; size is `r`. This is the same data you will keep when switching to numpy/Skia.

## Limitations

Overlap is last-wins per pixel. Z-ordering comes in Phase 024.

## Next phase preview

Phase 013 — Compare `list[Node]` against a `Scene` container (same code, clearer intent).
