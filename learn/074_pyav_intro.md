# Phase 074 — PyAV intro

## Goal of this phase

Explain why **PyAV** fits the “no subprocess ffmpeg” rule while still using battle-tested **libav** codecs.

## Problem being solved

Reimplementing H.264 is not an option. Controlling the **API surface** in-process is.

## Implementation

```python
# pip install av
# conceptual import only; API changes across versions, consult docs
# import av
# container = av.open(path, mode="w")
# stream = container.add_stream("h264", rate=30)
# for packet in stream.encode(frame):
#     container.mux(packet)
# container.close()
```

## Explanation

The tutorial keeps pseudocode: PyAV is **nontrivial**; ManimLite’s `export` module is the right place to centralize the real version-pinned code.

## Limitations

Codec availability depends on the libav build behind your wheel/conda; document supported platforms.

## Next phase preview

Phase 075 — H.264 stream: `pix_fmt`, `yuv420p`, timestamps.
