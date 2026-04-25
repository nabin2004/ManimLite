# Phase 025 — Grouping with `children`

## Goal of this phase

Introduce a **tree**: `Group` holds a list of drawables and draws them in order (relative coordinates next phase).

## Problem being solved

Scenes with dozens of parts need **structure**—axes, brackets, and equation pieces want sub-assemblies.

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
            c.draw(frame)


@dataclass
class Scene:
    w: int
    h: int
    root: Group

    def render(self) -> list[list[str]]:
        f = [[" " for _ in range(self.w)] for _ in range(self.h)]
        self.root.draw(f)
        return f


if __name__ == "__main__":
    g = Group()
    g.add(Pixel(2, 1))
    g.add(Pixel(3, 1))
    s = Scene(8, 3, g)
    for row in s.render():
        print("".join(row))
```

## Explanation

This is a **scene graph in embryo**: a root `Group` with `children`. Transforms (Phase 051+) will apply to groups.

## Limitations

No parent transforms: children are still in absolute grid coordinates.

## Next phase preview

Phase 026 — **Recursive** semantics (groups inside groups) with the same `draw` pattern.
