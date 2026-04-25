# Phase 068 — `Scene.save` API

## Goal of this phase

Sketch a **user-facing** call with explicit parameters: path, resolution, fps, duration, audio path optional.

## Problem being solved

If paths and options are global flags, LLM code becomes brittle and unreproducible.

## Implementation

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class RenderConfig:
    width: int = 1920
    height: int = 1080
    fps: float = 30.0
    duration: float = 5.0
    out: Path = Path("out.mp4")
    audio_path: Path | None = None


# def save(scene: Scene, cfg: RenderConfig) -> None: ...
```

## Explanation

A single `config` object is easy to pass around, log, and snapshot in bug reports.

## Limitations

No preset profiles (720p, vertical video) in this file—trivial to add as constructors.

## Next phase preview

Phase 069 — **Errors** you should expect: bad timeline bounds, IO failures, import errors for optional backends.
