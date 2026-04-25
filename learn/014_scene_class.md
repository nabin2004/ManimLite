# Phase 014 — `Scene` class

## Goal of this phase

Turn `Scene` into a small, explicit API: **dimensions** + **nodes** + a single **render** entry.

## Problem being solved

Scattered `blank()` + manual loops is error-prone. A scene is the *unit of composition* in animation tools.

## Implementation

We add type hints and a simple `add` helper.

```python
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Protocol


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
            if 0 <= x < len(frame[0]) and 0 <= y < len(frame):
                frame[y][x] = self.ch[0]


class Drawable(Protocol):
    def draw(self, frame: list[list[str]]) -> None: ...


@dataclass
class Scene:
    width: int
    height: int
    nodes: list[Drawable] = field(default_factory=list)

    def add(self, node: Drawable) -> None:
        self.nodes.append(node)

    def render(self) -> list[list[str]]:
        frame = [[" " for _ in range(self.width)] for _ in range(self.height)]
        for n in self.nodes:
            n.draw(frame)
        return frame


if __name__ == "__main__":
    s = Scene(40, 12)
    s.add(Disc(10, 6, 3))
    s.add(Disc(28, 6, 2))
    for row in s.render():
        print("".join(row))
```

## Explanation

`Protocol` gives static typing without inheritance: anything with `draw(frame)` is a `Drawable`. This is the engine’s public shape.

## Limitations

Still ASCII; still flat list (no `children` on nodes). Protocol does not help at runtime (duck typing still applies).

## Next phase preview

Phase 015 — `Scene.render` variations (background char, clear color concept).
