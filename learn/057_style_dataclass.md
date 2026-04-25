# Phase 057 — `Style` dataclass

## Goal of this phase

Model **fill** vs **stroke** explicitly so later renderers (Skia) map 1:1 to `Paint` concepts.

## Problem being solved

A single `rgba` is not enough for outlined shapes, dashed strokes, and joint styles.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Paint:
    rgba: tuple[float, float, float, float]  # 0..1


@dataclass
class Style:
    fill: Paint | None
    stroke: Paint | None
    stroke_width: float = 0.0
```

## Explanation

`None` fill means “no fill”; `None` stroke means “no stroke” (outline-only with fill `None` is valid for lines).

## Limitations

Gradients, patterns, and blend modes are out of scope for the tutorial’s core.

## Next phase preview

Phase 058 — A short case study: *composition* beats a subclass for “styled circle with shadow.”
