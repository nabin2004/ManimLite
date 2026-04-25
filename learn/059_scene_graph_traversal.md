# Phase 059 — Scene graph traversal (pre-order)

## Goal of this phase

Define **order of drawing** for nested groups: pre-order walk visits parent before children; painter’s order is list order among siblings.

## Problem being solved

If traversal is undefined, so is occlusion.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


class Node(Protocol):
    name: str


@dataclass
class Leaf:
    name: str


@dataclass
class G:
    name: str
    children: list[Node] = field(default_factory=list)


def pre_order(n: G | Leaf) -> list[str]:
    if isinstance(n, Leaf):
        return [n.name]
    out: list[str] = [n.name]
    for c in n.children:
        if isinstance(c, G):
            out += pre_order(c)
        else:
            out += pre_order(c)  # type: ignore[arg-type]
    return out
```

(Adjust for your exact types; a simple recursive visitor is the point.)

## Explanation

**Hit testing** (later) may use *reverse* pre-order. Rendering uses forward order. Document both if you add interaction.

## Limitations

No culling, no z-buffer—2D order only.

## Next phase preview

Phase 060 — **Bounding box** in world space: cheap culling, layout, and camera fit.
