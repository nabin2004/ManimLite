# Phase 064 — Skia sketch (no full implementation)

## Goal of this phase

Justify **Skia** as the vector/AA backend while keeping the tutorial off a heavy install until needed.

## Problem being solved

CPU nested loops for circles and text are not acceptable for a general engine. You want **antialiased paths** and good text at reasonable speed.

## Implementation

API sketch only—do not require `skia` in the minimal path.

```python
# skia_renderer.py (concept)
# pip install skia-python

# import skia
# def render_to_rgba(w, h, draw_cb):
#     surface = skia.Surface(w, h)
#     with surface as canvas:
#         draw_cb(canvas)
#     return surface.makeImageSnapshot().toArray(...)  # shape depends on API
```

## Explanation

`skia-python` binds Chromium’s engine and matches the “2D + text + quality” requirement without dragging LaTeX.

## Limitations

Native wheels, platform quirks, and binary size; keep it optional in packaging if your core goal is slimmer (tradeoffs).

## Next phase preview

Phase 065 — `Renderer` vs `Exporter` responsibilities.
