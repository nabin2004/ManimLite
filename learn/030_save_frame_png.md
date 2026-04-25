# Phase 030 — Save one frame as PNG

## Goal of this phase

Write a **single frame** to disk for debugging. This is **not** the hot video path (forbidden for long animations), but essential for eyeballing numpy output.

## Problem being solved

You need a viewer for RGBA buffers. Pillow is small, common, and maps 1:1 to `PIL.Image.fromarray`.

## Implementation

**Dependency:** `pillow` — justified as the minimal “save PNG” path without dragging in an entire GUI stack.

```bash
# pip install pillow numpy
```

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image


def new_frame(h: int, w: int) -> np.ndarray:
    return np.zeros((h, w, 4), dtype=np.uint8)


@dataclass
class Circle:
    cx: int
    cy: int
    r: int
    rgba: tuple[int, int, int, int] = (200, 90, 90, 255)

    def draw(self, frame: np.ndarray) -> None:
        h, w, _ = frame.shape
        r2 = self.r * self.r
        for y in range(max(0, self.cy - self.r), min(h, self.cy + self.r + 1)):
            for x in range(max(0, self.cx - self.r), min(w, self.cx + self.r + 1)):
                if (x - self.cx) ** 2 + (y - self.cy) ** 2 <= r2:
                    frame[y, x] = self.rgba


def save_rgba(path: str | Path, frame: np.ndarray) -> None:
    Image.fromarray(frame, mode="RGBA").save(path)


if __name__ == "__main__":
    f = new_frame(64, 96)
    f[:, :, :] = (18, 18, 24, 255)
    Circle(48, 32, 14).draw(f)
    save_rgba("frame0.png", f)
    print("wrote frame0.png")
```

## Explanation

`Image.fromarray` expects H×W×4 `uint8` for RGBA. This is a **one-off I/O** tool; the engine’s video path will stream in-memory to PyAV (no per-frame files).

## Limitations

Writing PNGs per frame in a 30 fps minute-long render is a performance disaster—Phase 050/073 emphasize streaming instead.

## Next phase preview

Phase 031 — `t` in `[0,1]`, `lerp`, the mathematical core of animation.
