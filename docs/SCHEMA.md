# MotionGram YAML Manifest Schema (v1.0)

Declarative scene files for MotionGram. YAML `type` values map 1:1 to Node classes in the component registry; timeline animations map to existing animators.

## Top-level structure

```yaml
version: "1.0"

lecture:          # optional metadata
  title: "..."
  subtitle: "..."
  author: "..."
  series: "..."
  language: en
  description: "..."
  voiceover: audio/full.mp3    # parsed; audio mux deferred in v1
  subtitles: subtitles/full.vtt

canvas:           # defaults for all scenes
  width: 1920
  height: 1080
  background: "#21252b"
  fps: 30

output:
  file: lecture.mp4
  codec: h264     # reserved; v1 always uses libx264

options:
  generate_section_titles: true
  section_title_duration: 3s
  section_title_style:
    font_size: 72
    color: "#ffffff"
    background: "#000000cc"

scenes: []        # flat list (quick demos)
sections: []      # grouped scenes for lectures
```

Either `scenes` or `sections` (or both) must be present.

## Sections

```yaml
sections:
  - id: norms_and_weight_decay
    title: "3.7.1 Norms and Weight Decay"
    description: "L2 norm and penalty term."
    scenes:
      - id: l2_norm_explanation
        duration: 12s
        elements: [...]
```

When `options.generate_section_titles` is true, a synthetic title scene is inserted before each section's scenes.

## Scene block

```yaml
- id: weight_decay_intro
  duration: 12s
  canvas: { background: "#ffffff" }   # optional override (background merge deferred in v1)
  voiceover: audio/scene.mp3
  subtitles: subtitles/scene.vtt      # or inline cue list
  camera:
    initial: { position: [960, 540], zoom: 1.0 }
    animations:
      - type: camera_pan
        from: [960, 540]
        to: [1200, 600]
        start: 2s
        duration: 4s
  elements:
    - id: weight_matrix
      type: Matrices
      properties:
        x: 80
        y: 200
        values: [[0.2, -0.5], [0.8, 0.3]]
        label: W
      animations:
        - type: animate_int_attribute
          attribute: highlight_row
          from: 0
          to: 2
          start: 0s
          duration: 6s
          easing: ease_in_out_cubic
  animations:                         # scene-level (camera, etc.)
    - type: fade_in
      target: scene
      start: 0s
      duration: 1s
  recipe:                             # optional sugar
    type: ForwardPass
    layers: [layer_input, layer_hidden, layer_output]
    start: 1s
    duration: 6s
```

## Elements

| Field | Required | Description |
|-------|----------|-------------|
| `id` | yes | Unique within the scene; referenced by recipes and animation targets |
| `type` | yes | Component registry name (`Matrices`, `Text`, `Circle`, …) |
| `properties` | no | Constructor kwargs (dataclass fields) |
| `animations` | no | Timeline entries on this element |

### Property aliases

| YAML | Maps to |
|------|---------|
| `position: [x, y]` | `x`, `y` |
| `typst: "..."` | `typst_source` (for `MathExpr`) |

**Math uses Typst, not LaTeX.** Do not use `latex` keys.

## Time format

Durations and timestamps accept:

- Numbers: `12`, `0.5` (seconds)
- Strings: `"12s"`, `"0.5s"`

## Animation types

| `type` | Key fields |
|--------|------------|
| `move_x`, `move_y` | `from`, `to` |
| `fade_in`, `fade_out` | optional `from`, `to` (opacity endpoints) |
| `scale_x`, `scale_y` | `from`, `to` |
| `rotate` | `from`, `to` (radians) |
| `blur` | optional `from`, `to` |
| `circle_outline` | — |
| `animate_attribute` | `attribute`, `from`, `to` |
| `animate_int_attribute` | `attribute`, `from`, `to` |
| `camera_pan` | `from: [x,y]`, `to: [x,y]` |
| `camera_zoom` | optional `from`, `to` |
| `move_arc` | `x0`, `y0`, `x1`, `y1`, optional `arc_height` |
| `move_along_path` | `points: [[x,y], ...]` |
| `squash_stretch` | optional `amount`, `axis` |
| `parallel`, `sequence` | nested `animations` list |
| `delay` | `animation`, `window_start`, `window_end` |

All animations require `start` and `duration` at the timeline level (except nested children inside `parallel` / `sequence` / `delay`).

Optional `easing` wraps the animator in `TimeScale`. Known values: `linear`, `smoothstep`, `ease_in_quad`, `ease_out_quad`, `ease_in_out_quad`, `ease_in_cubic`, `ease_out_cubic`, `ease_in_out_cubic`.

Use `target: scene` (or omit on scene-level lists) for camera animations attached to `scene.root`.

## Recipes

| `type` | Fields | Behavior |
|--------|--------|----------|
| `ForwardPass` | `layers` (element ids), `start`, `duration` | Sequential `progress` 0→1 on each layer |

## Subtitles

Inline cues:

```yaml
subtitles:
  - start: 0s
    end: 2s
    text: "Hello $x^2$"    # Typst body
    plain: "Hello x squared"  # optional WebVTT plain text
```

Or a path to a `.vtt` file relative to the manifest directory.

## Component types (registry)

Core: `Node`, `Circle`, `Line`, `Polygon`, `BezierCurve`, `Arc`, `Sector`, `SemiCircle`, `Path`, `Rectangle`, `Ellipse`, `RegularPolygon`, `Sphere`, `Cube`, `Cylinder`, `Text`, `MathExpr`, `CodeBlock`.

Deep learning (from `motiongram.deeplearning`): `Matrices`, `Vectors`, `HiddenLayers`, `ActivationFunctions`, `Convolutions`, `Regularization`, `ForwardProp`, `BackwardProp`, and all other exported `Node` subclasses.

Run `python -c "from motiongram.manifest.registry import COMPONENT_REGISTRY; print(sorted(COMPONENT_REGISTRY))"` for the full list in your install.

## CLI

```bash
motiongram render examples/yaml/deeplearning_showcase.yaml -o out.mp4
```

YAML manifests use `canvas.background` for `SkiaRenderer.clear_color`. CLI `--width`, `--height`, and `--fps` override manifest canvas values.

## v1 limitations

- Voiceover paths are validated but **not muxed** into MP4 yet.
- Per-scene `canvas.background` overrides are not applied when merging sections (global background only).
- No arbitrary Python expressions in YAML.
