# Phase 002 — Design philosophy

## Goal of this phase

State the **design rules** that prevent the codebase from turning into a second ManimCE—especially for LLM-generated scenes.

## Problem being solved

Feature-rich engines tend toward **deep inheritance** and **implicit global state** (`self.play(...)` chains with hidden ordering). That is hard for humans and worse for models.

## Implementation

```python
# rules.py — conceptual; not imported by toy code
from __future__ import annotations

DESIGN_RULES = (
    "Prefer dataclasses + functions for public data",
    "Keep composition shallow: Scene holds nodes; nodes hold children",
    "Make time explicit: timeline entries are (t0, t1, target, animator)",
    "Avoid hidden singletons: no global 'current scene' in library code",
)
```

## Explanation

**Composition over inheritance** does not mean “no classes.” It means: *inherit for true subtyping* (a `Circle` *is* drawable), not for workflow (*MyScene* subclasses a magic base with 40 mixins).

**Explicit timelines** beat implicit play stacks for debugging: you can print the timeline and know what happens.

## Limitations

Rules are easy to state and hard to enforce without tests and API review. Phases 037+ make timelines concrete.

## Next phase preview

Phase 003 — Python 3.11+ and a minimal project layout (`uv`, one file per experiment).
