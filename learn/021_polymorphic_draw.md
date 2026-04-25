# Phase 021 — Polymorphic `draw()`

## Goal of this phase

Treat **all shapes the same** at the call site: `for s in scene: s.draw(frame)`.

## Problem being solved

`isinstance` chains are a sign you lost polymorphism. The scene should not care *which* shape it holds.

## Implementation

```python
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Protocol


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


@dataclass
class Line(Shape):
    x0: int = 0
    y0: int = 0
    x1: int = 1
    y1: int = 0

    def draw(self, frame: list[list[str]]) -> None:
        w, h = len(frame[0]), len(frame)
        dx, dy = abs(self.x1 - self.x0), abs(self.y1 - self.y0)
        sx, sy = (1 if self.x0 < self.x1 else -1, 1 if self.y0 < self.y1 else -1)
        err, x, y = dx - dy, self.x0, self.y0
        while True:
            if 0 <= x < w and 0 <= y < h:
                frame[y][x] = self.ch[0]
            if x == self.x1 and y == self.y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy


# Scene loop only sees draw()
@dataclass
class Scene:
    width: int
    height: int
    items: list[object]

    def render(self) -> list[list[str]]:
        frame = [[" " for _ in range(self.width)] for _ in range(self.height)]
        for s in self.items:
            s.draw(frame)
        return frame
```

## Explanation

`Scene.render` is polymorphic: it does not branch on `Circle` vs `Line`. This is the engine’s core *runtime* pattern.

## Limitations

`list[object]` is too wide—`Protocol` tightens it (next phase).

## Next phase preview

Phase 022 — `Drawable` protocol instead of a heavy base for everything.
