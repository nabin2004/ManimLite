# Phase 017 — `Line` shape

## Goal of this phase

Add a second primitive: **line segment** `(x0,y0)–(x1,y1)` using the same `draw(frame)` contract.

## Problem being solved

Real scenes mix curves and straight edges. If `Line` is missing, users fake it with many `Node` points—bad for animation.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Line:
    x0: int
    y0: int
    x1: int
    y1: int
    ch: str = "#"

    def draw(self, frame: list[list[str]]) -> None:
        w, h = len(frame[0]), len(frame)

        def setp(x: int, y: int) -> None:
            if 0 <= x < w and 0 <= y < h:
                frame[y][x] = self.ch[0]

        dx = abs(self.x1 - self.x0)
        dy = abs(self.y1 - self.y0)
        sx = 1 if self.x0 < self.x1 else -1
        sy = 1 if self.y0 < self.y1 else -1
        err = dx - dy
        x, y = self.x0, self.y0
        while True:
            setp(x, y)
            if x == self.x1 and y == self.y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy


if __name__ == "__main__":
    f = [["." for _ in range(40)] for _ in range(12)]
    Line(2, 2, 36, 10).draw(f)
    for row in f:
        print("".join(row))
```

## Explanation

We duplicate Bresenham here to keep the phase self-contained. Phase 019 will call that duplication out as a smell—then we fix it with a base class or shared utility.

## Limitations

Thickness 1 only; no caps/joins.

## Next phase preview

Phase 018 — `Rectangle` (axis-aligned) as filled or outline (outline here).
