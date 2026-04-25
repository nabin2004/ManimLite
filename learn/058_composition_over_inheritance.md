# Phase 058 — Composition over inheritance (case study)

## Goal of this phase

Model a **drop shadow** as a *second* shape behind, offset—**not** a `ShadowedCircle` subclass.

## Problem being solved

Inheritance for visual effects is how you get 40 classes. Composition keeps the scene graph as data.

## Implementation

Idea only:

```text
Group(
  child1 = filled_circle(color=black, offset=(2,2), alpha=0.2)  # shadow
  child2 = stroked_circle(color=white)  # main
)
```

In Python: two `Shape` objects in a `Group` with z-order = list order.

## Explanation

This is the same trick UI toolkits use: *layers*, not *classes*.

## Limitations

Soft shadows need blur; approximate with multiple offset circles or a real blur filter in a renderer.

## Next phase preview

Phase 059 — Systematic **graph traversal** for draw order (pre-order).
