# Phase 063 — `NumpyRenderer`

## Goal of this phase

Tie the toy `Circle` raster from Phase 029 into a `Renderer` object that **owns** buffer lifetime.

## Problem being solved

Scattering `new_frame` calls leads to double frees / wrong buffer sizes.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class NumpyRenderer:
    w: int
    h: int
    clear_rgba: tuple[int, int, int, int] = (0, 0, 0, 255)

    def new_frame(self) -> np.ndarray:
        f = np.zeros((self.h, self.w, 4), dtype=np.uint8)
        r, g, b, a = self.clear_rgba
        f[:, :, 0] = r
        f[:, :, 1] = g
        f[:, :, 2] = b
        f[:, :, 3] = a
        return f
```

## Explanation

`submit` in Phase 062 might mean “hand off to encoder”; here, “finished frame for preview/save”.

## Limitations

No MSAA, no layer compositing; single buffer.

## Next phase preview

Phase 064 — A **Skia** sketch: why `skia-python` is justified for vector text and quality paths.
