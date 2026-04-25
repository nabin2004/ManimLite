# Phase 073 — No disk frame pipeline (again, concretely)

## Goal of this phase

Show the back-of-napkin **cost** of `png0001.png` dumps vs in-memory feed.

## Problem being solved

The habit of “mkdir frames/” is so common it must be actively argued against in code reviews.

## Implementation

Fermi estimate in prose + tiny timing harness you can run locally (not in CI):

```python
# compare writing 1800 PNGs vs holding arrays in a list — expect orders of magnitude I/O
```

## Explanation

**Throughput** to SSD is high but syscall overhead + filesystem metadata + compression kills interactive iteration.

## Limitations

Debug mode *may* write frames—make it a flag, off by default.

## Next phase preview

Phase 074 — `PyAV` and libav via Python bindings, not a subprocess `ffmpeg` CLI for encoding.
