# Phase 026 — Recursive draw

## Goal of this phase

Nest **Group inside Group**; traversal is depth-first, pre-order.

## Problem being solved

Without a recursive order rule, you cannot build hierarchical objects (a bracket around a sub-diagram).

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


class Drawable(Protocol):
    def draw(self, frame: list[list[str]]) -> None: ...


@dataclass
class Pixel:
    x: int
    y: int
    ch: str = "#"

    def draw(self, frame: list[list[str]]) -> None:
        w, h = len(frame[0]), len(frame)
        if 0 <= self.x < w and 0 <= self.y < h:
            frame[self.y][self.x] = self.ch[0]


@dataclass
class Group:
    children: list[Drawable] = field(default_factory=list)

    def add(self, d: Drawable) -> None:
        self.children.append(d)

    def draw(self, frame: list[list[str]]) -> None:
        for c in self.children:
            c.draw(frame)  # if c is a Group, this recurses


if __name__ == "__main__":
    inner = Group([Pixel(5, 2, "1")])
    outer = Group([inner, Pixel(6, 2, "2")])
    f = [[" " for _ in range(12)] for _ in range(5)]
    outer.draw(f)
    for row in f:
        print("".join(row))
```

## Explanation

This is a classic **scene graph** render: visit nodes, draw leaves. The transform matrix will multiply into child coordinates later.

## Limitations

Still no transforms—`Pixel` is absolute, so `Group` is only a **logical** container until Phase 051.

## Next phase preview

Phase 027 — The ASCII world runs out of fidelity. Switch to a numeric framebuffer.
