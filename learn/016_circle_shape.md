# Phase 016 — `Circle` shape

## Goal of this phase

Rename and isolate the **circle** primitive as part of the vocabulary: `Circle` is a shape with `cx, cy, r`.

## Problem being solved

Calling everything `Disc` is fine until you add `Line` and `Rect`—consistent naming matters for API stability.

## Implementation

```python
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class Circle:
    cx: int
    cy: int
    r: int
    ch: str = "o"

    def draw(self, frame: list[list[str]]) -> None:
        w, h = len(frame[0]), len(frame)
        n = max(8, self.r * 8)
        for i in range(n):
            t = 2 * math.pi * i / n
            x = int(round(self.cx + self.r * math.cos(t)))
            y = int(round(self.cy + self.r * math.sin(t)))
            if 0 <= x < w and 0 <= y < h:
                frame[y][x] = self.ch[0]


# quick manual test
if __name__ == "__main__":
    frame = [[" " for _ in range(40)] for _ in range(12)]
    Circle(20, 6, 4).draw(frame)
    for row in frame:
        print("".join(row))
```

## Explanation

This is the same drawing code with a clearer type name. ManimLite’s real `Circle` will use Skia paths; the *data model* (`center + radius`) stays.

## Limitations

Outline only; filled circles are a different rasterization problem.

## Next phase preview

Phase 017 — `Line` segment between two points (Bresenham again, as a method).
