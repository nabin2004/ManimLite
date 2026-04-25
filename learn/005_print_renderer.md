# Phase 005 — Print renderer

## Goal of this phase

Represent a frame as a **2D grid** and print it—no dependencies, instant feedback.

## Problem being solved

You need a renderer before you deserve a renderer abstraction. A grid is the smallest honest model of “a frame.”

## Implementation

```python
from __future__ import annotations

WIDTH, HEIGHT = 32, 16
BG = " "


def blank_frame() -> list[list[str]]:
    return [[BG for _ in range(WIDTH)] for _ in range(HEIGHT)]


def show(frame: list[list[str]]) -> None:
    for row in frame:
        print("".join(row))


if __name__ == "__main__":
    f = blank_frame()
    show(f)
```

## Explanation

This is your first “framebuffer”: a list of rows, each a list of characters. It is slow, ugly, and perfect for learning.

## Limitations

Aspect ratio is fake; brightness is discrete; no color. This is intentional—rendering details would hide the graph structure you are about to build.

## Next phase preview

Phase 006 — Plot a single point—first drawing primitive.
