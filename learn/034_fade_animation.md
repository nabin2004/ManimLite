# Phase 034 — Fade in / out

## Goal of this phase

Add **opacity** to a drawable model and lerp it for fade in/out on the numpy buffer (conceptually) or a style field (data-first).

## Problem being solved

Position is not the only thing that moves—visibility does.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Fadable:
    opacity: float  # 0..1, conceptual


@dataclass
class FadeTo:
    start: float
    end: float

    def apply(self, f: Fadable, t: float) -> None:
        t = max(0.0, min(1.0, t))
        f.opacity = self.start + (self.end - self.start) * t


if __name__ == "__main__":
    s = Fadable(0.0)
    anim = FadeTo(0, 1)
    for t in (0, 0.25, 0.5, 0.75, 1.0):
        anim.apply(s, t)
        print(t, s.opacity)
```

## Explanation

When rendering, multiply color alpha by `opacity` before writing RGBA, or set style if your renderer supports it.

## Limitations

No premultiplied alpha discussion; compositing is simplified.

## Next phase preview

Phase 035 — `Scale` via `lerp` on a uniform scale factor.
