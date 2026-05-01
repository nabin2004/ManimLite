# Phase 098 — ManimCE comparison

## Goal of this phase

Be honest: Typmotion trades **ecosystem breadth** for **install size, cold path, and LLM ergonomics**.

## Problem being solved

“Why not use Manim?” needs a one-page engineering answer, not a flame war.

## Implementation

| Area | ManimCE | Typmotion direction |
|------|---------|---------------------|
| Math | LaTeX (powerful) | Typst → SVG (different syntax) |
| Vector | Cairo/Pango stack | Skia (planned) / numpy (teaching) |
| Video | often disk + subprocess | PyAV in-process stream |
| API | deep inheritance, `play()` | flat records + explicit timeline |
| 3D | available | not a goal (v0.x) |

## Explanation

This is a **wedge** product for 2D education online—not a feature-complete Manim port.

## Limitations

Manim’s community assets (templates, gallery) won’t port line-for-line.

## Next phase preview

Phase 099 — **Limitations** list of this tutorial’s toy code vs the real `typmotion` package.
