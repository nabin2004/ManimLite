# Phase 011 — `Node.draw()`

## Goal of this phase

Make the drawing contract obvious: **every node takes the same `frame` argument** and returns nothing, mutating the buffer.

## Problem being solved

Inconsistent `draw` signatures will block a scene graph and a renderer later. We lock the contract early.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass


WIDTH, HEIGHT = 40, 12
BG = "."


def blank() -> list[list[str]]:
    return [[BG for _ in range(WIDTH)] for _ in range(HEIGHT)]


def setp(f: list[list[str]], x: int, y: int, ch: str) -> None:
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        f[y][x] = ch[0]


@dataclass
class Node:
    x: int
    y: int
    ch: str = "#"

    def draw(self, frame: list[list[str]]) -> None:
        """Render into a character framebuffer."""
        setp(frame, self.x, self.y, self.ch)


def show(f: list[list[str]]) -> None:
    for row in f:
        print("".join(row))


if __name__ == "__main__":
    f = blank()
    n = Node(5, 5, "@")
    n.draw(f)
    show(f)
```

## Explanation

`draw(self, frame)` is the “micro-protocol.” Later, `frame` becomes a numpy array or a Skia canvas, but the call shape stays: **pass a target**, mutate it.

## Limitations

Still one glyph per `Node`—this is a stepping stone, not a shape engine.

## Next phase preview

Phase 012 — `x`/`y` are not the only state: introduce radius for a primitive circle (still ASCII).
