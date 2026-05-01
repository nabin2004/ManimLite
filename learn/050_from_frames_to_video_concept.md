# Phase 050 — From frames to video (concept, no disk dump)

## Goal of this phase

Describe the **end-to-end mental model**: `for frame in frames: encode.write(frame)`.

## Problem being solved

Many tutorials teach “export PNGs then ffmpeg.” That violates ManimLite’s I/O and subprocess constraints. The right mental model is **streaming memory to an encoder** (PyAV, Phase 074).

## Implementation

Pseudocode only—no I/O in this file.

```python
# Conceptual: iterator of HxWx4 uint8 in display order
def frames() -> "Iterator[np.ndarray]":
    for i in range(n):
        yield render_frame(i)


def encode_to_mp4(frames, path):
    # PyAV: open H.264 stream, set time_base, write packets, flush
    ...
```

## Explanation

A **frame iterator** decouples *render* from *encode* so you can add audio without changing rasterization.

## Limitations

Color subsampling, B-frames, and timestamping are encoder details; Phase 075 scratches the surface.

## Next phase preview

Phase 051 — `Transform` dataclass: the uniform way to position/scale groups.
