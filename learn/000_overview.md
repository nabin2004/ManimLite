# Phase 000 — Overview

## Goal of this phase

Set expectations: what this `learn/` path is, what hard rules apply, and how to read the 101 files (000–100).

## Problem being solved

Without a map, “build an engine from scratch” becomes either too abstract or a random walk. This phase pins **scope** and **constraints** before any code.

## Implementation

There is no executable code here—only the contract for the series.

```text
Rules (non-negotiable for MotionGram direction):
1. No LaTeX / TeX Live in the tutorial’s learning path.
2. No subprocess-based video encoding (no `ffmpeg` CLI as the render path).
3. No writing every frame to disk as PNG/JPG in the hot path (disk frame pipeline).
4. Conceptual in-memory frames: numpy arrays or similar, then encode in-process (PyAV later).
5. Keep the *teaching* API flat: prefer dataclasses + explicit parameters over deep trees.
```

## Explanation

Each phase file is **one idea**. Early phases use a **print-based** “screen” so you can see pixels without installing heavy graphics stacks. Once the pain of functions-only code is clear, we add **classes** where they buy real encapsulation—not before.

Later bands add **animation as time**, **scene graphs**, **renderer protocols**, and finally **PyAV-based** export—always with the constraints above.

## Limitations

This is a **pedagogical** sequence, not a drop-in replacement for the `motiongram` package’s production code. Some phases show “bad” code on purpose so the next phase can fix it.

## Next phase preview

Phase 001 — Motivation: why ManimCE’s weight and cold path are the real enemy, and what we optimize for instead.
