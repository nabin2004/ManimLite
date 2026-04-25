# Phase 024 — Z-ordering

## Goal of this phase

Define **occlusion** for the flat list case: `nodes` is drawn in order; last draw wins for a pixel.

## Problem being solved

If you can’t state ordering rules, “who is in front” becomes accidental.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass


def setp(f: list[list[str]], x: int, y: int, ch: str) -> None:
    w, h = len(f[0]), len(f)
    if 0 <= x < w and 0 <= y < h:
        f[y][x] = ch[0]


@dataclass
class Pixel:
    x: int
    y: int
    ch: str

    def draw(self, f: list[list[str]]) -> None:
        setp(f, self.x, self.y, self.ch)


@dataclass
class Scene:
    w: int
    h: int
    items: list[object]

    def render(self) -> list[list[str]]:
        f = [[" " for _ in range(self.w)] for _ in range(self.h)]
        for it in self.items:  # painter's order
            it.draw(f)
        return f


if __name__ == "__main__":
    s = Scene(12, 3, [Pixel(3, 1, "A"), Pixel(3, 1, "B")])  # B overwrites A
    for row in s.render():
        print("".join(row))
```

## Explanation

Later, groups and transforms will complicate this. For a flat `Scene`, **list order = z-index baseline**.

## Limitations

No true layers with blend modes. No per-layer compositing.

## Next phase preview

Phase 025 — Nesting: `Node` with `children` to build simple diagrams.
