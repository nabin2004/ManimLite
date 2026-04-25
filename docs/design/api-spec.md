# Public API specification (contract)

**Status:** Pre-alpha — names are stable enough for docs; behavior is mostly stubbed.

## Package entry

- **`import manimlite`**
- **Re-exported symbols (intended public):** `Scene`, `Node`, `Timeline`, `Text`, `MathExpr`, `CodeBlock`, `VoiceOver`, `KittenVoiceOverBackend`, `__version__`

Additional symbols remain importable from submodules (`shapes`, `animate`, etc.) but may move until v0.2.

## Core

### `Scene`

- **Constructor kwargs:** `width`, `height`, `fps`, `duration`, optional `root`, `timeline`
- **Methods:**
  - `narrate(voice_over: VoiceOver) -> None` — register narration (implementation will append to an internal audio list)

### `Node`

- **Fields:** `children`
- **Methods:** `draw(canvas)`

### `Timeline`

- **Fields:** `entries: tuple[tuple[float, float, Node, Any], ...]`
- **Methods:** `add(start, end, target, animator) -> Timeline`

## Shapes (`manimlite.shapes`)

- `Circle(radius, fill_color, stroke_color?, stroke_width)`
- `Line(x0, y0, x1, y1, stroke_color, stroke_width)`
- `Polygon(vertices, fill_color, stroke_color?, stroke_width)`

## Text (`manimlite.text`)

- `Text(content, font_size, color)`
- `MathExpr(typst_source, font_size, color)`
- `CodeBlock(code, language, font_size)`

## Animation (`manimlite.animate`)

- `Animation(name)` with `as_animator() -> Animator`
- **`Animator` protocol:** `apply(node, t: float) -> None`

## Easing (`manimlite.easing`)

- `linear(t)`
- `ease_in_out_quad(t)`
- `cubic_bezier(t, p1x, p1y, p2x, p2y)` — stub returns `t` until implemented

## Render / export

- `SkiaRenderer(scene).render_frame(time) -> Any`
- `PyAVEncoder(scene, output_path).encode(frame_source) -> None`

## Audio (`manimlite.audio` and top-level re-exports)

- `VoiceOver(text, voice="Jasper", start=0.0)` — `voice` is a Kitten built-in name when using `KittenVoiceOverBackend`
- `KittenVoiceOverBackend(model_name="KittenML/kitten-tts-nano-0.8-int8", speed=1.0, clean_text=False)`
- `VoiceOverBackend` protocol — `synthesize(text, *, voice: str) -> bytes` (WAV bytes for the Kitten path)
- `AudioMixer(sample_rate).mix(segments) -> Any`

## CLI

- `manimlite render <scene.py>`

## Versioning policy (planned)

- **SemVer** after 1.0; pre-1.0 minor bumps may break API with changelog entries.
