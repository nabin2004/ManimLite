# Phase 044 — Callable animator

## Goal of this phase

Replace tiny animation classes with **`Callable[[object, float], None]`** when state updates are ad hoc.

## Problem being solved

A class with only `apply` and no state is a function wearing a tuxedo.

## Implementation

```python
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

Animator = Callable[["Obj", float], None]


@dataclass
class Obj:
    x: float


def make_move(sx: float, ex: float) -> Animator:
    def apply(o: Obj, t: float) -> None:
        t = max(0.0, min(1.0, t))
        o.x = sx + (ex - sx) * t

    return apply


if __name__ == "__main__":
    o = Obj(0.0)
    anim = make_move(0, 5)
    anim(o, 0.5)
    print(o.x)
```

## Explanation

The closure captures `sx,ex`—this is a **factory** pattern. LLMs handle factories better when effects are data (`start`, `end`) rather than class names.

## Limitations

Harder to serialize than a pure datamodel—Phases 045–047 bridge that with explicit records.

## Next phase preview

Phase 045 — Dataclass animators with a uniform `apply` method and no inheritance fan-out.
