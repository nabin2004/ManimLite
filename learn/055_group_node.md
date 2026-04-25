# Phase 055 — `Group` as a `Node`

## Goal of this phase

Unify: **both** leaves and `Group` expose `draw` and carry `children` (empty for leaves) or a clear protocol split.

## Problem being solved

If `Group` is special-cased in 10 places, you get bugs. A small inheritance or protocol unifies traversal.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

import numpy as np


class Drawable(Protocol):
    def draw(self, xform: "XF", target: np.ndarray) -> None: ...


@dataclass
class XF:
    x: float = 0.0
    y: float = 0.0
    s: float = 1.0


@dataclass
class Group:
    xf: XF
    children: list[Drawable] = field(default_factory=list)

    def draw(self, parent: XF, target: np.ndarray) -> None:
        world = self._compose(parent, self.xf)
        for c in self.children:
            c.draw(world, target)  # each child obeys the same (world_xf, target) call shape

    @staticmethod
    def _compose(p: XF, c: XF) -> XF:
        return XF(p.x + p.s * c.x, p.y + p.s * c.y, p.s * c.s)
```

## Explanation

`draw` takes the **parent** transform so the recursion is explicit. Leaves ignore `children`.

## Limitations

This sketch elides a lot of `Circle.draw` code—focus stays on the call shape.

## Next phase preview

Phase 056 — `Shape` = `geometry + style + transform` split.
