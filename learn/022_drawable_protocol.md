# Phase 022 — `Drawable` protocol

## Goal of this phase

Use **`typing.Protocol`** so anything with `draw(frame)` is drawable, even if it is **not** a `Shape` subclass (text, image, effect layers).

## Problem being solved

Inheritance boxes you in. Protocols let you add new drawable kinds without touching a base class.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class Drawable(Protocol):
    ch: str  # optional: protocols can require attrs in typing, be careful
    def draw(self, frame: list[list[str]]) -> None: ...


# Better: only require the method, not ch
class PDrawable(Protocol):
    def draw(self, frame: list[list[str]]) -> None: ...


@dataclass
class Label:
    text: str
    x: int
    y: int

    def draw(self, frame: list[list[str]]) -> None:
        # crude single-line text
        w, h = len(frame[0]), len(frame)
        for i, ch in enumerate(self.text):
            x = self.x + i
            y = self.y
            if 0 <= x < w and 0 <= y < h:
                frame[y][x] = ch


@dataclass
class Scene:
    width: int
    height: int
    items: list[PDrawable]  # in real code, default_factory=list

    def render(self) -> list[list[str]]:
        frame = [[" " for _ in range(self.width)] for _ in range(self.height)]
        for s in self.items:
            s.draw(frame)
        return frame
```

## Explanation

`Label` is *not* a `Shape` subclass, but it fits the protocol. This is the heart of “composition + protocols” in modern Python.

## Limitations

`Protocol` checks are for static type checkers, not at runtime, unless you use `@runtime_checkable` (rarely needed here).

## Next phase preview

Phase 023 — Add color? Not in ASCII. Add a **color field** for future renderers and store it, even if unused.
