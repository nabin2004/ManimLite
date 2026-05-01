# Phase 085 — Async and threading

## Goal of this phase

Name safe parallel patterns: **encode thread** feeding from a **render queue**; not magic `async` on CPU raster without care.

## Problem being solved

The GIL means pure Python raster often won’t speed up with threads; **encode** in C (libav) can overlap with **render** if pipelined.

## Implementation

Concept:

```text
[render thread] -> queue of frames -> [encode thread] -> file
```

## Explanation

Measure before parallelizing. Deadlocks and duplicated buffers are more likely than a speedup in toy scenes.

## Limitations

Multiprocess render needs picklable state or shared memory; avoid until necessary.

## Next phase preview

Phase 086 — A **CLI** `typmotion render file.py:SceneName`.
