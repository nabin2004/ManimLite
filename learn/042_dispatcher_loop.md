# Phase 042 — Dispatcher loop

## Goal of this phase

For global time `T`, compute **active timeline entries** and a **local** `t in [0,1]` for each.

## Problem being solved

The engine’s heart is: *given `T`, what happens?* Not *given a frame index without a clock*.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Entry:
    t0: float
    t1: float
    name: str


def local_t(T: float, t0: float, t1: float) -> float | None:
    if T < t0 or T > t1 or t1 == t0:
        return None
    return (T - t0) / (t1 - t0)


def active(T: float, entries: list[Entry]) -> list[tuple[Entry, float]]:
    out: list[tuple[Entry, float]] = []
    for e in entries:
        u = local_t(T, e.t0, e.t1)
        if u is not None:
            out.append((e, u))
    return out


if __name__ == "__main__":
    e = [Entry(0, 1, "a"), Entry(0.5, 1.5, "b")]
    for T in (0, 0.25, 0.75, 1.25):
        print(T, active(T, e))
```

## Explanation

Parallel tracks appear as *multiple* active entries. Sequential tracks simply do not overlap.

## Limitations

If two entries target the same property and overlap, *both apply*—you must design timelines to avoid conflicts or add priorities.

## Next phase preview

Phase 043 — Why dozens of `class MoveEasedRotateShimmer` is unmaintainable.
