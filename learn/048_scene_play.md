# Phase 048 — `Scene.play` (conceptual)

## Goal of this phase

Define **how user code** schedules: `play(move(circle, ...))` vs explicit timeline data.

## Problem being solved

LLMs and humans need a **one obvious way** to add animations. Data-first `Timeline` (Phase 037) and sugar `play` can coexist if `play` *only* appends entries.

## Implementation (sketch)

```python
from __future__ import annotations

from dataclasses import dataclass, field, replace


@dataclass(frozen=True, slots=True)
class Entry:
    t0: float
    t1: float
    kind: str


@dataclass
class Scene:
    t_cursor: float = 0.0
    entries: tuple[Entry, ...] = ()

    def play(self, duration: float, kind: str) -> "Scene":
        t0, t1 = self.t_cursor, self.t_cursor + duration
        e = Entry(t0, t1, kind)
        return replace(self, t_cursor=t1, entries=(*self.entries, e))
```

## Explanation

A **cursor** gives sequential `play` for free. Parallel tracks are explicit: use absolute times or a second `Scene` line—don’t magic-global `current time`.

## Limitations

No nested calls; a real `play` will take `target` and `animator` objects.

## Next phase preview

Phase 049 — `render N frames`: global `T` goes `0..duration` in steps of `1/fps`.
