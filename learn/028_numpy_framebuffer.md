# Phase 028 — NumPy framebuffer

## Goal of this phase

Create an **H×W×4** `uint8` array as a blank canvas, cleared to a background color.

## Problem being solved

You need a data structure you can pass to a video encoder and (later) a vector renderer. NumPy is the default lingua franca for pixel buffers in Python.

## Implementation

**Dependency (justify once):** `numpy` is the standard n-dimensional array for image rows; alternatives exist (`memoryview` + `array.array`) but PyAV examples and scientific stacks assume NumPy.

```bash
# pip install numpy
```

```python
from __future__ import annotations

import numpy as np


def new_frame(h: int, w: int) -> np.ndarray:
    # RGBA, top-left origin, row i is scanline i (y down)
    return np.zeros((h, w, 4), dtype=np.uint8)


def clear(frame: np.ndarray, rgba: tuple[int, int, int, int]) -> None:
    r, g, b, a = rgba
    frame[:, :, 0] = r
    frame[:, :, 1] = g
    frame[:, :, 2] = b
    frame[:, :, 3] = a


if __name__ == "__main__":
    f = new_frame(4, 6)
    clear(f, (30, 30, 40, 255))
    print(f.shape, f.dtype)
```

## Explanation

`uint8` matches common 8-bit color paths. The shape `(H, W, 4)` is easy to `reshape` to `(H*W*4,)` for raw encoder input if required.

## Limitations

No color management (sRGB vs linear) yet—educational projects often ignore it until it bites.

## Next phase preview

Phase 029 — `set_pixel` on a numpy image with alpha overwrite.
