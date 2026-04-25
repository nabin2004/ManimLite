# Phase 066 — Frame iterator

## Goal of this phase

Define the exporter-facing API as `Iterator[ndarray]` (or a typed protocol) to stream frames.

## Problem being solved

If exporters accept only `list[ndarray]`, you will materialize 30×60 seconds of 1080p in RAM.

## Implementation

```python
from __future__ import annotations

from collections.abc import Iterator
from typing import Protocol

import numpy as np


class FrameStream(Protocol):
    def __iter__(self) -> Iterator[np.ndarray]: ...


def iter_uniform(scene_render, n: int) -> Iterator[np.ndarray]:
    for i in range(n):
        yield scene_render(i)
```

## Explanation

A generator (`yield`) is the Pythonic stream. The encoder pulls frames as fast as it can encode.

## Limitations

Backpressure and parallel decode/encode are advanced (Phase 085).

## Next phase preview

Phase 067 — A **time-driven loop** that steps `T` and pulls frames.
