# Phase 056 — `Shape` = geometry + style + transform

## Goal of this phase

Split responsibilities so you can **reuse** geometry (unit circle) with different styles, and **animate** `xf` and style independently.

## Problem being solved

A monolith `Circle` with 15 fields is hard to extend and to generate via LLM.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class XF:
    x: float
    y: float
    s: float = 1.0


@dataclass
class Style:
    rgba: tuple[int, int, int, int] = (200, 200, 200, 255)


@dataclass
class CircleGeom:
    r: float = 1.0  # in local space


@dataclass
class Shape:
    xf: XF
    style: Style
    geom: CircleGeom

    # draw() would use geom.r * xf.s, etc.
```

## Explanation

This mirrors Typmotion’s design direction: **flat** records with a few well-named parts instead of 6-level inheritance.

## Limitations

More boilerplate; win is clarity and testability.

## Next phase preview

Phase 057 — Flesh out `Style` (stroke vs fill) without implementing Skia yet.
