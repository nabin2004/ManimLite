# Phase 083 — Chunked encoding

## Goal of this phase

Avoid holding **all frames** in RAM: render and encode in chunks, flushing encoder state properly.

## Problem being solved

A 1-hour 1080p float32 buffer list is not going to fit on a laptop.

## Implementation

Pattern:

```text
for chunk in time_chunks:
    for T in chunk:
        encode_one_frame(T)
    # optionally flush or reset scratch buffers
```

## Explanation

**Streaming** is an algorithm property, not a library trick: your scene evaluation must be restartable or strictly forward-only in time (usually true).

## Limitations

Seeking/rewind for effects that need future frames (filters) complicates one-pass—avoid those in v0.

## Next phase preview

Phase 084 — **Determinism** for goldens: seeds, `float` rounding, parallel reductions.
