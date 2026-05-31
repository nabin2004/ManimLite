# Phase 088 — Config

## Goal of this phase

Layer configuration: **defaults** in code, **overrides** from CLI, optional **.motiongram.toml** later.

## Problem being solved

Seventeen `if os.getenv` checks scattered in code = unmaintainable.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass, fields
import os


@dataclass
class Config:
    width: int = 1920
    height: int = 1080
    fps: float = 30.0


def from_env() -> Config:
    c = Config()
    w = os.getenv("MOTIONGRAM_WIDTH")
    if w:
        c.width = int(w)
    return c
```

## Explanation

A single `Config` class is the LLM’s friend; partial overrides via `dataclasses.replace`.

## Limitations

Schema validation (pydantic) is optional; keep dependencies lean early.

## Next phase preview

Phase 089 — **Debug overlay**: time `T`, frame `i`, simple grid.
