# Phase 037 — Timeline tuples

## Goal of this phase

Represent a schedule of animations as **data**: `(t_start, t_end, target_id, animator)`.

## Problem being solved

If animations are implicit method calls, you cannot serialize, print, or reorder them. **Flat records** are LLM-friendly.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TimelineEntry:
    t0: float
    t1: float
    target: str
    kind: str


@dataclass(frozen=True, slots=True)
class Timeline:
    entries: tuple[TimelineEntry, ...] = ()

    def add(self, e: TimelineEntry) -> "Timeline":
        return Timeline((*self.entries, e))
```

## Explanation

This mirrors MotionGram’s `Timeline` type: *immutable append* is easy to reason about, friendly to parallel tooling.

## Limitations

`target` is a string id here—real code uses `Node` object identity or stable ids.

## Next phase preview

Phase 038 — `Scene` gains `.animate(...)` to append entries (API sugar).
