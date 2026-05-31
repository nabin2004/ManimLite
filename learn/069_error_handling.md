# Phase 069 — Error handling

## Goal of this phase

List **actionable** failure modes: timeline bounds, missing Typst, missing optional TTS, PyAV init failure.

## Problem being solved

A generic `Exception` is an LLM trap—typed errors and messages speed debugging 10×.

## Implementation

```python
from __future__ import annotations


class MotionGramError(Exception):
    """Base."""


class TimelineError(MotionGramError):
    pass


def check_entry(t0: float, t1: float, duration: float) -> None:
    if t0 < 0 or t1 > duration or t0 > t1:
        raise TimelineError(f"bad entry {t0=}, {t1=}, {duration=}")
```

## Explanation

Keep the hierarchy small: **5–8** error types is enough for a long time.

## Limitations

Localization of messages is a product concern, not a tutorial one.

## Next phase preview

Phase 070 — **Testing** strategy: unit (math), property (easing), golden (raster hash).
