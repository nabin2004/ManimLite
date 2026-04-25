# Phase 062 — `Renderer` protocol

## Goal of this phase

Introduce a **Renderer** that consumes a scene graph and writes pixels—so `Scene` is not hard-coded to numpy.

## Problem being solved

If `draw` methods take `np.ndarray` directly, you cannot swap in Skia or a headless test double.

## Implementation

```python
from __future__ import annotations

from typing import Protocol

import numpy as np


class Renderer(Protocol):
    width: int
    height: int

    def new_frame(self) -> np.ndarray: ...
    def submit(self, frame: np.ndarray) -> None: ...


class NumpyBufferRenderer:
    def __init__(self, w: int, h: int) -> None:
        self.width = w
        self.height = h

    def new_frame(self) -> np.ndarray:
        return np.zeros((self.height, self.width, 4), dtype=np.uint8)

    def submit(self, frame: np.ndarray) -> None:
        _ = frame
```

## Explanation

A production engine often passes a **context** (Skia `Canvas`, Cairo `Context`) instead of a final buffer, but the **separation of concerns** is the same: graph → emit draw calls → target.

## Limitations

Protocol methods cannot enforce shape at runtime; tests + mypy help.

## Next phase preview

Phase 063 — A minimal `NumpyRenderer` that clears and calls node draws.
