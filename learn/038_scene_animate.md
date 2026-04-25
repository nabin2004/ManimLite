# Phase 038 — `Scene` records entries

## Goal of this phase

Make `Scene` own a **`Timeline`**: `scene = scene.queue_move(...)` or `scene.add_entry(...)`.

## Problem being solved

The scene is the natural owner of *what happens when*; nodes own *what* they are; animators own *how to interpolate*.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any


@dataclass(frozen=True, slots=True)
class TimelineEntry:
    t0: float
    t1: float
    target: str
    name: str


@dataclass
class Scene:
    duration: float = 3.0
    timeline: tuple[TimelineEntry, ...] = field(default_factory=tuple)

    def with_entry(
        self,
        t0: float,
        t1: float,
        target: str,
        name: str,
    ) -> "Scene":
        e = TimelineEntry(t0, t1, target, name)
        return replace(self, timeline=(*self.timeline, e))


if __name__ == "__main__":
    s0 = Scene()
    s1 = s0.with_entry(0, 1, "c0", "move")
    s2 = s1.with_entry(1, 2, "c0", "fade")
    print(s2.timeline)
```

## Explanation

Immutability makes debugging trivial: you can print `s0/s1/s2` to see history. A mutable engine is fine in production, but the **shape** of the data stays the same.

## Limitations

No evaluation yet—`name` is not dispatched (Phase 042).

## Next phase preview

Phase 039 — Parallel vs sequential: overlapping `t` ranges vs back-to-back.
