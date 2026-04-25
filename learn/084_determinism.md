# Phase 084 — Determinism

## Goal of this phase

Make **repro** possible: for the same `Scene`, `RenderConfig`, and seed, the output hash matches across runs on one machine.

## Problem being solved

Flaky goldens are worse than no tests—they train people to delete tests.

## Implementation

Tactics:

```python
# random.seed(0)
# float env flags (avoid non-deterministic thread reductions if any)
# pin library versions
```

## Explanation

Cross-machine determinism for video is **hard** (encoder, threading). Aim first for **in-machine** repro; broaden later.

## Limitations

GPU backends often introduce nondeterminism—CPU paths first.

## Next phase preview

Phase 085 — **Async and threads**—when to parallelize *encode* vs *render* (careful with GIL).
