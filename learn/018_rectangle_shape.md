# Phase 018 — `Rectangle` shape

## Goal of this phase

Add an **axis-aligned rectangle** outline—four edges with simple integer bounds.

## Problem being solved

Text panels, underlines, and hit boxes are rectangles. This completes a minimal primitive set: **Circle, Line, Rect**.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Rect:
    x: int
    y: int
    w: int
    h: int
    ch: str = "#"

    def draw(self, frame: list[list[str]]) -> None:
        fw, fh = len(frame[0]), len(frame)
        x0, y0 = self.x, self.y
        x1, y1 = self.x + self.w - 1, self.y + self.h - 1
        for x in range(x0, x1 + 1):
            for y in (y0, y1):
                if 0 <= x < fw and 0 <= y < fh:
                    frame[y][x] = self.ch[0]
        for y in range(y0, y1 + 1):
            for x in (x0, x1):
                if 0 <= x < fw and 0 <= y < fh:
                    frame[y][x] = self.ch[0]


if __name__ == "__main__":
    f = [[" " for _ in range(40)] for _ in range(12)]
    Rect(5, 2, 30, 8).draw(f)
    for row in f:
        print("".join(row))
```

## Explanation

This draws the **perimeter** by visiting top/bottom runs and left/right runs (corners are written twice; harmless for ASCII).

A filled rectangle would use a double loop over the interior; outline matches how UI borders are often thought about.

## Limitations

No rounded corners, no stroke width, no subpixel alignment.

## Next phase preview

Phase 019 — The duplication across `Circle`/`Line`/`Rect` is now visible—time to DRY *without* a framework.
