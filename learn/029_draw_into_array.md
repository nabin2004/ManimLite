# Phase 029 — `draw` into a NumPy array

## Goal of this phase

Re-implement a **red circle** as filled-ish pixels: many points, alpha 255, simple distance test.

## Problem being solved

You need a bridge between *geometry* and *pixels* before Skia. A distance field on a grid is a crude software raster.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def new_frame(h: int, w: int) -> np.ndarray:
    return np.zeros((h, w, 4), dtype=np.uint8)


def clear(frame: np.ndarray, rgba: tuple[int, int, int, int]) -> None:
    r, g, b, a = rgba
    frame[:, :, 0] = r
    frame[:, :, 1] = g
    frame[:, :, 2] = b
    frame[:, :, 3] = a


@dataclass
class Circle:
    cx: int
    cy: int
    r: int
    rgba: tuple[int, int, int, int] = (200, 90, 90, 255)

    def draw(self, frame: np.ndarray) -> None:
        h, w, _ = frame.shape
        r2 = self.r * self.r
        y0, y1 = max(0, self.cy - self.r), min(h, self.cy + self.r + 1)
        x0, x1 = max(0, self.cx - self.r), min(w, self.cx + self.r + 1)
        for y in range(y0, y1):
            for x in range(x0, x1):
                dx, dy = x - self.cx, y - self.cy
                if dx * dx + dy * dy <= r2:
                    frame[y, x, 0:4] = self.rgba


if __name__ == "__main__":
    f = new_frame(32, 48)
    clear(f, (20, 22, 30, 255))
    Circle(24, 16, 10).draw(f)
    print("alpha center:", f[16, 24, 3])
```

## Explanation

This is O(r²) in the bounding box; Skia is better. The point is **data flow**: `draw` mutates a numpy buffer you can also feed to a movie encoder.

## Limitations

No antialiasing; jagged edge; no gamma.

## Next phase preview

Phase 030 — **Pillow** to save a PNG (minimal I/O) so you can inspect pixels outside the terminal.
