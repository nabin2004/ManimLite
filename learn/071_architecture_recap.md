# Phase 071 — Architecture recap

## Goal of this phase

Consolidate the story: **Scene graph → raster at T → frame stream → PyAV → file** (optional audio).

## Problem being solved

After 070 files of growth, readers need a single diagram in words.

## Implementation

```text
Scene (nodes + timeline)
  -> evaluate at T (dispatchers)
  -> Renderer (numpy or skia)
  -> uint8 HxWx4 frame
  -> Exporter (PyAV) muxed with audio
```

## Explanation

Each boundary exists to **swap** one part without touching others. That is the “systems” view.

## Limitations

This is not microservice distribution—one Python process is fine for v0.x.

## Next phase preview

Phase 072 — **Profiling** where the cost actually is (often not the math you think).
