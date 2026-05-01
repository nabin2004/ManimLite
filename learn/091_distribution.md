# Phase 091 — Distribution

## Goal of this phase

Outline shipping: **wheels** on PyPI, **sdist**, and optional **Docker** with pinned Typst/kittentts where needed.

## Problem being solved

“Clone from source” is fine for devs; teachers want `pip install typmotion`.

## Implementation

Checklist:

```text
- version semver + changelog
- test matrix linux/mac (windows later)
- document native deps (if any) clearly
- optional dockerfile for air-gapped classrooms
```

## Explanation

Distribution is a **policy** and **ops** problem as much as code; keep the wheel small, extras explicit.

## Limitations

Binary wheels (skia) drive platform support—state supported combinations honestly.

## Next phase preview

Phase 092 — **Plugin** registration for new shapes (entry points or registry pattern).
