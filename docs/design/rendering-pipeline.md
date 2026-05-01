# Rendering pipeline

## Goals

- No per-frame PNG sequence on disk for the default path
- Deterministic frame content at given `(scene, t)`
- Math via Typst with aggressive caching

## Phases

1. **Load / validate** — import scene module; validate timeline bounds; resolve asset paths.
2. **Prepare** — build Skia surfaces, load fonts, warm Typst cache for all `MathExpr` nodes.
3. **Rasterize** — for each frame index `i`, compute `t = i / fps`; apply active animators; traverse graph; issue Skia draw calls.
4. **Encode** — feed `numpy`/`bytes` RGB(A) buffers into PyAV video stream; set time_base from fps.
5. **Mux** — attach audio if present; finalize MP4.

## Frame buffer format (implemented)

- **Color space:** sRGB
- **Layout:** Skia image snapshot → NumPy row-major **RGBA8888** `uint8` (`SkiaRenderer.render_frame`). Encoder strips alpha to **RGB24** for libx264.

## Typst integration

1. Build a minimal Typst document wrapping user expression (font/size/color injected).
2. Run Typst CLI or library (implementation choice) with stdin/stdout or temp **RAM** fs if required.
3. Parse SVG; **hash** normalized SVG string + typst version → disk cache path `~/.cache/manimlite/typst/<hash>.svg`.
4. Parse SVG paths into Skia paths (or rasterize SVG to texture once).

## Encoder settings (defaults, tunable later)

- **Video:** H.264, yuv420p, CFR from `scene.fps`
- **Audio:** AAC or PCM re-encode as needed for container compatibility

## Failure modes

- Encoder init failure → clear error with libav log tail
- Typst failure → stderr captured, mapped to `MathExprCompileError`

## Related

- [SDD.md](SDD.md) runtime diagrams
- ADR-0001, ADR-0002, ADR-0003
