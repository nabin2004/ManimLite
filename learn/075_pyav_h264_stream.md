# Phase 075 — H.264 stream (sketch)

## Goal of this phase

List the **non-obvious** encoder decisions that affect playability: pixel format, color range, and CFR.

## Problem being solved

A video that “plays on my machine” but not in browsers usually failed **yuv420p** or botched time_base.

## Implementation

```text
Checklist (conceptual):
- convert RGBA -> yuv420p (swscale inside libav or your code)
- set average bitrate or crf (encoder-specific)
- set time_base = 1/fps for CFR
- write header, packets, trailer
```

## Explanation

**PyAV** exposes libav structures; the mental model is still: **Frame → encode → Packet → mux**.

## Limitations

Hardware encoders (NVENC/VA-API) are a separate ADR; start with **software** `libx264` for repeatability.

## Next phase preview

Phase 076 — **PCM** audio buffers aligned to the same time axis as video frames.
