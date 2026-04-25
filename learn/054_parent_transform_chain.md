# Phase 054 — Parent transform chain

## Goal of this phase

Compute **world XF** for a node by walking from root: `xf_world = id; for a in path: xf_world = compose(xf_world, a.xf)`.

## Problem being solved

Without a chain rule, `Group` is cosmetic.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class XF:
    x: float = 0.0
    y: float = 0.0
    s: float = 1.0


def compose(outer: XF, inner: XF) -> XF:
    return XF(outer.x + outer.s * inner.x, outer.y + outer.s * inner.y, outer.s * inner.s)


@dataclass
class Node:
    xf: XF
    name: str = "n"


@dataclass
class Group:
    xf: XF
    name: str = "g"
    children: list[Node] | None = None

    def __post_init__(self) -> None:
        if self.children is None:
            object.__setattr__(self, "children", [])


def world_of_child(parent: XF, child: Node) -> XF:
    return compose(parent, child.xf)


if __name__ == "__main__":
    root = Group(XF(10, 0, 2), "root", [Node(XF(5, 0, 1), "a")])
    w = world_of_child(root.xf, root.children[0])
    print(w)
```

## Explanation

A full engine stores **parent pointers** or a path stack; the fold is the same.

## Limitations

No caching of world XFs; later you can add dirty flags (Phase 061).

## Next phase preview

Phase 055 — A `Group` that *is* a `Node` in the OOP sense.
