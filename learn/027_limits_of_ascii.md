# Phase 027 — Limits of ASCII

## Goal of this phase

**Retire the character grid** as the primary model: you need a continuous **color buffer** to represent antialiasing, fills, and video.

## Problem being solved

ASCII taught coordinates and order; it is not a target for a video engine. Sticking to it any longer would mislead you about **memory layout** and **throughput**.

## Implementation

No code—just a checklist of what a real buffer needs:

```text
- 2D array of shape (H, W, 4) for RGBA8, row-major, top-left origin
- clear color each frame
- set_pixel / line / circle that write floats or bytes, not glyphs
- later: the same data feeds PyAV (Phase 074+)
```

## Explanation

The jump from `list[list[str]]` to `ndarray` is the first **dependency trade**: NumPy (or raw `array.array`) is justified because image buffers are big and performance-sensitive.

## Limitations

You still are not “GPU” yet; numpy is CPU-side.

## Next phase preview

Phase 028 — `numpy` framebuffer, minimal dependency on **NumPy only**.
