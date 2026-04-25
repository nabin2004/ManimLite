# Data model

## Scene

| Field | Type | Description |
| ----- | ---- | ----------- |
| `width` | `int` | Pixel width |
| `height` | `int` | Pixel height |
| `fps` | `float` | Frames per second |
| `duration` | `float` | Scene length in seconds |
| `root` | `Node` | Scene graph root |
| `timeline` | `Timeline` | Animation entries |

## Node

- **Base:** `children: tuple[Node, ...]`
- **Drawing:** `draw(canvas: Any) -> None` (Skia canvas type to be pinned in `render.py`)
- **Primitives:** `Circle`, `Line`, `Polygon` extend `Node` with geometry fields.

## Timeline

- **Immutable-style updates:** `Timeline.add(start, end, target, animator) -> Timeline` returns new timeline (or mutation TBD; current stub is immutable append).

## Animation tuple

`(start: float, end: float, target: Node, animator: Any)`

- **Invariant:** `0 <= start < end <= scene.duration` (validated at render prep).

## VoiceOver

| Field | Type | Description |
| ----- | ---- | ----------- |
| `text` | `str` | Utterance |
| `voice` | `str` | Kitten built-in voice name (e.g. `Jasper`, `Luna`; see upstream `available_voices`) |
| `start` | `float` | Timeline position in seconds |

## Protocols

- **`Drawable`** — `draw(canvas) -> None` (alias of `Node` contract).
- **`Animator`** — `apply(node, t: float) -> None` with `t` eased.
- **`VoiceOverBackend`** — `synthesize(text, *, voice: str) -> bytes`.

## Future extensions

- **Transform** node: matrix stack for groups
- **Style** tokens: shared fill/stroke palettes for themes
