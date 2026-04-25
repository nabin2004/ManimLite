# Phase 089 — Debug overlay

## Goal of this phase

Add non-production drawing: frame counter, time `T`, and optional bounds boxes—gated by a `debug` flag.

## Problem being solved

“Why did this clip 1-frame glitch?” is impossible without on-screen time diagnostics.

## Implementation

Idea: after rasterizing, draw text with a tiny 5×7 font or just render debug into stderr each frame in slow mode.

## Explanation

**Overlay** in-image is shareable; **stderr** logs are local dev only.

## Limitations

Debug text must not change production goldens; disable in CI unless snapshot tests account for it.

## Next phase preview

Phase 090 — `pyproject.toml`, extras, and lockfile (`uv`).
