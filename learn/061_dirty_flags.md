# Phase 061 — Dirty flags (concept)

## Goal of this phase

Show how engines avoid redoing work: mark nodes **dirty** when animated; clear after rasterization.

## Problem being solved

Full re-render every frame is fine for 1080p software at 10 fps, not for larger scenes.

## Implementation (idea-level)

```python
class Node:
    dirty: bool = True


def mark_dirty(n: Node) -> None:
    n.dirty = True


def render_and_clear(n: Node) -> None:
    if n.dirty:
        # draw
        n.dirty = False
```

## Explanation

A real system propagates dirty bits up the tree, batches updates, and may separate **transform dirty** from **content dirty**.

## Limitations

Over-invalidation bugs are common—keep the first engine simple, add caching after profiling (Phase 072).

## Next phase preview

Phase 062 — `Renderer` protocol: separate **raster** from **scene** structure.
