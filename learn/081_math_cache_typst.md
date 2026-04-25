# Phase 081 — Math cache (Typst concept)

## Goal of this phase

Explain how to avoid LaTeX: **Typst → SVG → Skia path/raster**, cached by **hash(Typst source + engine version)**.

## Problem being solved

Recompiling identical math every frame is wasted; caching is mandatory with a text-based math path.

## Implementation

```python
import hashlib


def cache_key(src: str, typst_version: str) -> str:
    h = hashlib.sha256((typst_version + "\n" + src).encode()).hexdigest()
    return f"typst_{h}.svg"
```

## Explanation

The **hot path** loads cached SVG; **cache miss** runs Typst offline and stores the SVG in `~/.cache/manimlite/typst/...`.

## Limitations

Typst errors need good error mapping; subpixel differences between SVG renderers can affect goldens.

## Next phase preview

Phase 082 — **Font** loading and caching for text (not math).
