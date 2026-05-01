# Phase 010 — First `Node` class

## Goal of this phase

Introduce the **smallest** class: something drawable that owns a **position** and knows how to **draw** into a frame.

## Problem being solved

You need a named unit of state (`x`, `y`) plus a method (`draw`) that stays next to that state. That is OOP in one bite—not frameworks.

## Implementation

We keep the ASCII world for a little longer. `Node` is abstract-ish: a base you will specialize.

```python
from __future__ import annotations

import math
from dataclasses import dataclass

WIDTH, HEIGHT = 32, 16
BG = " "


def blank() -> list[list[str]]:
    return [[BG for _ in range(WIDTH)] for _ in range(HEIGHT)]


def setp(f: list[list[str]], x: int, y: int, ch: str) -> None:
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        f[y][x] = ch[0]


@dataclass
class Node:
    x: int = 0
    y: int = 0
    ch: str = "o"

    def draw(self, frame: list[list[str]]) -> None:
        setp(frame, self.x, self.y, self.ch)


def show(f: list[list[str]]) -> None:
    for row in f:
        print("".join(row))


if __name__ == "__main__":
    f = blank()
    Node(10, 8, "A").draw(f)
    Node(20, 8, "B").draw(f)
    show(f)
```

## Explanation

`@dataclass` makes `__init__` and `repr` free. The method `draw` is the core protocol of Typmotion’s graph: *nodes know how to render themselves* into a target buffer.

Inheritance is not required yet. We start with a concrete `Node` that is really a “point object.”

## Limitations

Everything is a single character; not yet a `Circle` shape. No scene container—just ad hoc `draw` calls.

## Next phase preview

Phase 011 — Add `draw` expectations and separate “marker node” from real geometry.
