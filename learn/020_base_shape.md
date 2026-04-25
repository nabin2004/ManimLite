# Phase 020 — Base `Shape`

## Goal of this phase

Use **one level of inheritance** to hold common fields (`ch` / style hook), not to capture all geometry.

## Problem being solved

Three `@dataclass` types repeating `ch: str` is noise. A base class is justified when the shared field is stable.

## Implementation

```python
from __future__ import annotations

import math
from dataclasses import dataclass


def setp(frame: list[list[str]], x: int, y: int, ch: str) -> None:
    w, h = len(frame[0]), len(frame)
    if 0 <= x < w and 0 <= y < h:
        frame[y][x] = ch[0]


@dataclass
class Shape:
    ch: str = "#"


@dataclass
class Circle(Shape):
    cx: int = 0
    cy: int = 0
    r: int = 1

    def draw(self, frame: list[list[str]]) -> None:
        n = max(8, self.r * 8)
        for i in range(n):
            t = 2 * math.pi * i / n
            x = int(round(self.cx + self.r * math.cos(t)))
            y = int(round(self.cy + self.r * math.sin(t)))
            setp(frame, x, y, self.ch)


# demonstration
if __name__ == "__main__":
    f = [[" " for _ in range(32)] for _ in range(10)]
    Circle(ch="O", cx=16, cy=5, r=3).draw(f)
    for row in f:
        print("".join(row))
```

## Explanation

`Shape` is not magical—it’s a place for shared defaults. The **behavior** is still in `Circle.draw`.

## Limitations

Inheritance can pull you toward a deep tree; stop at *one* level unless a second subtype truly shares behavior.

## Next phase preview

Phase 021 — `Line` and `Rect` also subclass `Shape` and all share a uniform `draw`.
