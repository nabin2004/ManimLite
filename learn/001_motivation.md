# Phase 001 — Motivation

## Goal of this phase

Name the **concrete problems** MotionGram-style engines try to fix: install size, cold start, I/O-bound encoding, and LLM-unfriendly APIs.

## Problem being solved

“Faster animation” is vague. We need targets you can measure: time to first frame, bytes on disk, and whether a generated script compiles on the first try.

## Implementation

No library code—just a checklist you can reuse as a benchmark spec.

```python
# metrics.py — sketch only, not a dependency of later phases
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Budget:
    """Targets for a future MotionGram benchmark (illustrative numbers)."""

    max_cold_start_s: float = 5.0  # 10s scene, laptop-class CPU
    max_core_install_mb: int = 100
    forbid_latex: bool = True
    forbid_ffmpeg_subprocess_encode: bool = True
    forbid_disk_frame_dump_in_hot_path: bool = True
```

## Explanation

Manim Community Edition is excellent, but its ecosystem often pulls **TeX**, **Cairo**, and **disk + subprocess ffmpeg** workflows. For many **2D educational** clips, most wall time is **not** animation math—it is **toolchain and I/O**.

MotionGram aims to keep the **animation model** simple while making the **render/export path** cheap: in-memory frames, in-process mux/encode, flat APIs.

## Limitations

Budget numbers are **not** guarantees in this tutorial—they are **design pressure**. Real benchmarks belong in CI later.

## Next phase preview

Phase 002 — Design philosophy: composition, shallow hierarchies, explicit time.
