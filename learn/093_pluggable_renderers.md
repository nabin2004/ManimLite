# Phase 093 — Pluggable renderers

## Goal of this phase

Select `Renderer` at runtime: `numpy` (debug) vs `skia` (quality) vs a **null** renderer for headless server tests (counts draw calls only).

## Problem being solved

Test suites should not need GPUs or giant raster buffers for logic tests.

## Implementation

```python
def make_renderer(kind: str, w: int, h: int):
    if kind == "numpy":
        return NumpyRenderer(w, h)
    if kind == "skia":
        return SkiaRenderer(w, h)  # when available
    raise ValueError(kind)
```

## Explanation

A **NullRenderer** (stats only) is surprisingly useful: ensures scene graph walks happen without I/O.

## Limitations

Parity of output between renderers is not automatic—separate baselines or tolerance tests per backend.

## Next phase preview

Phase 094 — Pluggable **animators** (library vs user-defined).
