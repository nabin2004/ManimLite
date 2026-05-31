# Public API specification (contract)

**Status:** Pre-alpha — core Skia / Typst / PyAV paths are functional; some areas remain stubs.

## Package entry

- **`import motiongram`**
- **Re-exported symbols (intended public):** `Scene`, `Node`, `Timeline`, `Text`, `MathExpr`, `CodeBlock`, `PyAVEncoder`, `SkiaRenderer`, `MoveX`, `MoveY`, `VoiceOver`, `KittenVoiceOverBackend`, `__version__` (among others; see `motiongram.__all__`)

Additional symbols remain importable from submodules (`shapes`, `animate`, etc.) but may move until v0.2.

### `motiongram.procedural` (optional, explicit import)

- Not part of ``motiongram.__all__`` — import explicitly, e.g. ``from motiongram.procedural import RainyLandscapeManifest, materialize_rainy_landscape``.
- Holds **preset manifests** and builders that populate a `world_shell()` and schedule `Scene.add_animation` from data; stable engine APIs remain ``motiongram.world`` + timeline primitives.

## Core

### `Scene`

- **Constructor kwargs:** `width`, `height`, `fps`, `duration`, optional `root`, `timeline`, optional `subtitle_track`
- **Methods:**
  - `narrate(voice_over: VoiceOver) -> None` — register narration (implementation will append to an internal audio list)

### `Node`

- **Fields:** `children`
- **Methods:** `draw(canvas)`

### `Timeline`

- **Fields:** `entries: tuple[tuple[float, float, Node, Any], ...]`
- **Methods:** `add(start, end, target, animator) -> Timeline`

## Shapes (`motiongram.shapes`)

- `Circle(radius, fill_color, stroke_color?, stroke_width)`
- `Line(x0=, y0=, x1=, y1=, stroke_color, stroke_width)` — prefer keywords; positionals bind `Node` fields first.
- `Polygon(vertices, fill_color, stroke_color?, stroke_width)`

## Text (`motiongram.text`)

- `Text(content, font_size, color)`
- `MathExpr(typst_source, font_size, color)`
- `CodeBlock(code, language, font_size)`


## Subtitles (`motiongram.subtitles` and `Scene.subtitle_track`)

- **Types:** `SubtitleCue(start, end, typst, plain=None, voice=None, settings=None)`, `SubtitleStyle`, `SubtitleTrack(cues, style)` — `voice` / `settings` apply only to WebVTT output
- **Scene field:** `subtitle_track: SubtitleTrack | None` — burned into the frame **after** the camera pass (screen-fixed)
- **Time:** active when `start <= t < end` (half-open)
- **Helpers:** `validate_subtitle_track`, `active_subtitles`, `sort_cues`, `subtitle_typst_layout`, `write_webvtt` — spec-style timestamps (`.` ms separator, compact `MM:SS.mmm` under one hour); optional `<v …>` via `voice` and cue settings line via `settings`
- **Typst cache:** `cached_typst_subtitle_svg_path`, `typst_subtitle_cache_key`, `subtitle_document_for_cache`

## Animation (`motiongram.animate`)

- **`MoveX(x0, x1)`**, **`MoveY(y0, y1)`** — set `node.x` / `node.y` over the segment.
- `Animation(name)` with `as_animator() -> Animator`
- **`Animator` protocol:** `apply(node, t: float) -> None`

## Easing (`motiongram.easing`)

- `linear(t)`
- `ease_in_out_quad(t)`
- `cubic_bezier(t, p1x, p1y, p2x, p2y)` — stub returns `t` until implemented

## Render / export

- `SkiaRenderer(clear_color=(r,g,b)).render_frame(scene, time) -> ndarray` — H×W×4 RGBA `uint8`.
- `PyAVEncoder(scene, output_path, renderer=SkiaRenderer()).encode(verbose=...) -> Path` — muxes H.264 MP4 via PyAV.

## Audio (`motiongram.audio` and top-level re-exports)

- `VoiceOver(text, voice="Jasper", start=0.0)` — `voice` is a Kitten built-in name when using `KittenVoiceOverBackend`
- `KittenVoiceOverBackend(model_name="KittenML/kitten-tts-nano-0.8-int8", speed=1.0, clean_text=False)`
- `VoiceOverBackend` protocol — `synthesize(text, *, voice: str) -> bytes` (WAV bytes for the Kitten path)
- `AudioMixer(sample_rate).mix(segments) -> Any`

## CLI

- `motiongram render <scene.py> [-o OUT] [--width W] [--height H] [--fps F] [-q]` — loads `build_scene()` or module-level `scene`; optional `get_skia_renderer()` in the same module for custom `SkiaRenderer`.

## Versioning policy (planned)

- **SemVer** after 1.0; pre-1.0 minor bumps may break API with changelog entries.
