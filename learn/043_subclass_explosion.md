# Phase 043 — Subclass explosion

## Goal of this phase

**Show the antipattern**: one `Animation` subclass per combination of effects.

## Problem being solved

Inheritance for *cartesian product features* (move×fade×rotate) explodes. Data-driven animators avoid that.

## Implementation

**Do not do this in production code:**

```python
class MoveFade: ...
class MoveRotate: ...
class FadeRotate: ...
# ... combinatorial explosion
```

**Prefer:** one `TweenAttr` with parameters (Phase 046).

## Explanation

OOP is good for true **subtyping** (`Circle` vs `Line`). It is a poor tool for *feature combinations*—that is a **data** problem (timeline rows + parametric animators).

## Limitations

Sometimes a specialized animator is justified (Bezier paths)—keep those rare and documented.

## Next phase preview

Phase 044 — `Animator = Callable` or a tiny protocol, not a class per effect.
