# Phase 013 — List of nodes vs `Scene`

## Goal of this phase

Show that a plain `list` of drawables is almost enough—and why a **`Scene` wrapper** is still useful.

## Problem being solved

A list is a container, but a scene is a *policy*: width/height, background, maybe future camera and time. You want one object to `render()`.

## Implementation

```python
from __future__ import annotations

import math
from dataclasses import dataclass, field

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


@dataclass
class Scene:
    width: int
    height: int
    nodes: list[object] = field(default_factory=list)

    def render(self) -> list[list[str]]:
        frame = [[" " for _ in range(self.width)] for _ in range(self.height)]
        for n in self.nodes:
            n.draw(frame)  # duck typing for now
        return frame


def show(f: list[list[str]]) -> None:
    for row in f:
        print("".join(row))


if __name__ == "__main__":
    s = Scene(WIDTH, HEIGHT, [Disc(12, 7, 4), Disc(28, 7, 3)])
    show(s.render())
```

## Explanation

`Scene.render` is the first **orchestrator**: it owns dimensions and the draw order. The list `nodes` is the scene graph in its flattest form (no nesting yet).

## Limitations

`list[object]` is too loose. Typing and protocols fix this next.

## Next phase preview

Phase 014 — Tighten `Scene` (typing) and a clearer `__init__` story.
