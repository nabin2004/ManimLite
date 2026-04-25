# Phase 040 — Easing

## Goal of this phase

Implement a few scalar maps `f: [0,1] -> [0,1]` so motion **accelerates and decelerates** instead of being linear in wall time.

## Problem being solved

Linear `t` often feels mechanical. Easing is the cheapest upgrade.

## Implementation

```python
from __future__ import annotations


def linear(t: float) -> float:
    return t


def ease_in_out_quad(t: float) -> float:
    t = max(0.0, min(1.0, t))
    if t < 0.5:
        return 2 * t * t
    return 1 - ((-2 * t + 2) ** 2) / 2


if __name__ == "__main__":
    for t in (0, 0.25, 0.5, 0.75, 1.0):
        print(t, ease_in_out_quad(t))
```

## Explanation

Animators will call `eased = ease( local_t_in_segment )` where `local_t` maps segment wall time to `0..1` first.

## Limitations

No physics-based spring—keep it explicit and cheap.

## Next phase preview

Phase 041 — Plumb easing into a `Move.apply` that takes an easing function.
