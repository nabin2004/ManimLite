# ADR-0002: Use Typst-to-SVG instead of LaTeX for math

- **Status:** Accepted
- **Date:** 2025-04-25

## Context

LaTeX/TeX Live dominates install size and cold-start time for math-heavy Manim workflows. Educational scenes rarely need full TeX compatibility.

## Decision

Render math via **Typst**, producing **SVG** imported into Skia, with a **content-hash cache** to avoid redundant compilation.

## Consequences

- **Positive:** Drastically smaller toolchain than TeX Live; faster iteration.
- **Negative:** Not LaTeX-compatible; users must learn Typst syntax subset supported by MotionGram wrappers.
- **Follow-up:** Ship pinned Typst version; structured errors mapping Typst diagnostics to user source.
