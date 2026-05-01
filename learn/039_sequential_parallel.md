# Phase 039 — Sequential vs parallel

## Goal of this phase

Define two scheduling shapes on the **same timeline**:

- **Parallel:** overlapping intervals `[t0, t1]` for different properties or nodes.
- **Sequential:** `t1` of one equals `t0` of the next (or use a `cursor`).

## Problem being solved

“Play after” vs “at the same time” is where animation APIs become subtle.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class E:
    t0: float
    t1: float
    who: str


def is_parallel(a: E, b: E) -> bool:
    return not (a.t1 <= b.t0 or b.t1 <= a.t0)


a = E(0, 1, "A")
b = E(0.5, 1.5, "B")
print("overlap?", is_parallel(a, b))
```

## Explanation

ManimCE’s `Play`/`Wait` is one encoding; ManimLite prefers an explicit time axis: **if intervals overlap, effects overlap**.

## Limitations

No dependency edges (“B after A ends”)—you can compute with a cursor helper later.

## Next phase preview

Phase 040 — Easing: warp `t` before lerp with `ease_in_out_quad` etc.
