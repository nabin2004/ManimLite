# Phase 047 — Property-based animation (typed)

## Goal of this phase

Avoid raw strings: enumerate **which channel** to tween (`X`, `Y`, `OPACITY`).

## Problem being solved

`TweenFloat` by name is fragile. A `Channel` or small union of known fields is LLM- and refactor-friendly.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class Ch(Enum):
    X = auto()
    Y = auto()
    OP = auto()


@dataclass
class Obj:
    x: float
    y: float
    opacity: float = 1.0


@dataclass(frozen=True, slots=True)
class Tween:
    ch: Ch
    a: float
    b: float

    def apply(self, o: Obj, t: float) -> None:
        t = max(0.0, min(1.0, t))
        v = self.a + (self.b - self.a) * t
        if self.ch is Ch.X:
            o.x = v
        elif self.ch is Ch.Y:
            o.y = v
        else:
            o.opacity = v
```

## Explanation

`match`/`Enum` is verbose but *explicit*—a good public API for a few channels.

## Limitations

Adding a channel means editing `apply`—or switch to a mapping table (still explicit).

## Next phase preview

Phase 048 — `Scene.play(head_time, entry)` that advances a clock—conceptual.
