# Phase 065 — Renderer vs exporter

## Goal of this phase

Split **rasterization** (pixels in memory) from **multiplexing** (MP4/WEBM) so each part can be tested and swapped.

## Problem being solved

A monolith `render_video()` is impossible to reason about, profile, or mock.

## Implementation

Responsibility table:

| Component | Input | Output |
|----------|-------|--------|
| `Renderer` / scene | Scene @ time T | `HxWx4` uint8 |
| `AudioMixer` (optional) | Clips, timeline | PCM/AAC plan |
| `Exporter` (PyAV) | Frame iterator, audio | Muxed video file (or in-memory) |

Pseudocode:

```python
def export(renderer, scene, times, out_path):
    for T in times:
        frame = rasterize_at(scene, renderer, T)
        encoder.write_frame(frame)
    encoder.close(out_path)
```

## Explanation

This matches MotionGram’s `render` vs `export` modules: **two layers**, one policy (no per-frame temp files in hot path).

## Limitations

Timestamping, CFR vs VFR, and audio clock drift are exporter details; Phase 075–077 return.

## Next phase preview

Phase 066 — `Iterator` of frames as the core **protocol** for export.
