# Phase 031 — Lerp and `t`

## Goal of this phase

Define **animation** as numeric interpolation: at normalized time `t in [0,1]`, map start→end with `lerp(a,b,t)`.

## Problem being solved

Without this definition, “animation” is vague UI talk. The engine will always reduce to *numbers changing over time*.

## Implementation

```python
from __future__ import annotations


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def clamp01(t: float) -> float:
    return max(0.0, min(1.0, t))


if __name__ == "__main__":
    for i in range(5):
        t = i / 4
        print(t, lerp(0, 10, t))
```

## Explanation

Easing (Phase 040) is just `t' = f(t)` before lerp. Everything else—`Move`, `Scale`, `Fade`—reuses the same lerp story.

## Limitations

Linear lerp in RGB can look wrong (color should lerp in linear light). Ignored in early phases.

## Next phase preview

Phase 032 — A `Move` class that changes `x,y` of an object as `t` goes 0→1.
