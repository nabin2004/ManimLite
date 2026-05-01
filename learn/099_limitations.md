# Phase 099 — Limitations of this learn path

## Goal of this phase

List what the **101-phase tutorial** deliberately did not do, so you don’t assume it is production-ready.

## Problem being solved

A learning sequence must simplify; without a “what we left out” section, readers over-trust the toy code.

## Implementation

- Not pixel-perfect to Manim’s behavior
- Not a replacement for the repo’s [SRS/SDD](../docs/)
- **No** end-to-end Skia+Typst+PyAV integration in one file—**phases** split concerns
- Many snippets are **pseudocode** (PyAV, Skia) where deps would bloat
- Kitten/ML-sized extras are **off-core** in the real project

## Explanation

Use this `learn/` path to **build mental models**, then read `src/manimlite/` to see actual stubs and the CI-enforced style.

## Limitations

We cannot cover every platform bug you will meet (codec packs, fontconfig, wayland, etc.).

## Next phase preview

Phase 100 — **Final architecture** and reading order back into the real codebase.
