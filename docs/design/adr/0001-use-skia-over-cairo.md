# ADR-0001: Use Skia (skia-python) instead of Cairo for 2D rasterization

- **Status:** Accepted
- **Date:** 2025-04-25

## Context

ManimCE historically relies on Cairo/Pango for vector rendering. Cairo pulls native dependencies and complicates installs on minimal systems.

## Decision

Use **skia-python** as the primary rasterization engine for primitives, text (where applicable), and compositing.

## Consequences

- **Positive:** Mature GPU/CPU renderer; strong path/clip/mask; wheels for common platforms.
- **Negative:** Heavier than pure CPU toy renderers; binding version drift must be tracked in CI.
- **Follow-up:** Document minimum skia-python version per release; add visual regression harness when feasible.
