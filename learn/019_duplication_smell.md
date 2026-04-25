# Phase 019 — Duplication smell

## Goal of this phase

**Name the problem**: three shapes repeat patterns—bounds checks, `ch`, and `draw` routing.

## Problem being solved

If you DRY too early, you get a “God `Shape`” with 12 flags. The right first step is a **mechanical** duplicate: shared helpers, not a taxonomy.

## Implementation

Extract only what is shared: `setp` and maybe `w,h` queries.

```python
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Protocol


def frame_size(frame: list[list[str]]) -> tuple[int, int]:
    return len(frame[0]), len(frame)


def setp(frame: list[list[str]], x: int, y: int, ch: str) -> None:
    w, h = frame_size(frame)
    if 0 <= x < w and 0 <= y < h:
        frame[y][x] = ch[0]


@dataclass
class Circle:
    cx: int
    cy: int
    r: int
    ch: str = "o"

    def draw(self, frame: list[list[str]]) -> None:
        n = max(8, self.r * 8)
        for i in range(n):
            t = 2 * math.pi * i / n
            x = int(round(self.cx + self.r * math.cos(t)))
            y = int(round(self.cy + self.r * math.sin(t)))
            setp(frame, x, y, self.ch)
```

## Explanation

**Shared low-level paint** is safe to deduplicate. **Shared high-level class hierarchy** is not free—wait until the polymorphism story is real (Phases 020–021).

## Limitations

We still have three shape classes, not a hierarchy yet.

## Next phase preview

Phase 020 — Introduce a small base `Shape` to centralize *style-ish* data only if it pays rent.
