# Phase 015 — `Scene.render()`

## Goal of this phase

Make rendering a **pure function of state** (given fixed nodes): `render()` returns a new frame from `Scene` fields.

## Problem being solved

If you mutate one global frame across calls, double-rendering or partial updates become bugs. Each `render()` allocates a fresh buffer (still cheap at toy sizes).

## Implementation

```python
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Protocol


class Drawable(Protocol):
    def draw(self, frame: list[list[str]]) -> None: ...


@dataclass
class Disc:
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


@dataclass
class Scene:
    width: int
    height: int
    bg: str = "."
    nodes: list[Drawable] = field(default_factory=list)

    def add(self, n: Drawable) -> None:
        self.nodes.append(n)

    def render(self) -> list[list[str]]:
        frame = [[self.bg for _ in range(self.width)] for _ in range(self.height)]
        for n in self.nodes:
            n.draw(frame)
        return frame


if __name__ == "__main__":
    s = Scene(36, 10, bg=" ")
    s.add(Disc(10, 5, 3, "A"))
    s.add(Disc(24, 5, 3, "B"))
    f = s.render()
    for row in f:
        print("".join(row))
```

## Explanation

`bg` is a stand-in for clear color. In numpy you will clear to `(r,g,b,a)`; the idea is identical: **clear, then draw in order**.

## Limitations

No camera, no transforms—just top-left coordinates in screen space.

## Next phase preview

Phase 016 — Name `Circle` explicitly and split `Disc` from other shapes.
