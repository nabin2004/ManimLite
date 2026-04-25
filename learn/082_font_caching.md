# Phase 082 — Font caching

## Goal of this phase

Describe **why** fonts are stateful and expensive: shaping, kerning, hinting.

## Problem being solved

Loading a TTF per string is catastrophic; Skia’s `Typeface` objects should be **reused**.

## Implementation

Policy sketch:

```text
key = (path|bytes hash, size)
cache[key] = SkiaTypeface or freetype face
```

## Explanation

Match your text API to what your renderer needs: **UTF-8 strings** in, **glyph runs** internally.

## Limitations

RTL scripts, vertical text, and emoji require a real shaper (HarfBuzz path in Skia).

## Next phase preview

Phase 083 — **Chunked encoding** to cap memory on long renders.
