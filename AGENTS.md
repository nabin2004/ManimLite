# Agent / LLM authoring guide (ManimLite)

This file helps humans and **LLM agents** write scenes that match ManimLite’s intended public API.

## Design principles

1. **Flat over deep inheritance** — prefer `@dataclass` nodes and explicit composition over subclass trees.
2. **Explicit timelines** — animations are tuples `(start_time, end_time, target, animator)` attached to a scene, not implicit method call chains.
3. **Typed surfaces** — use type hints on public constructors and protocols (`Drawable`, `Animator`).
4. **Small vocabulary** — fewer top-level concepts than ManimCE: `Scene`, `Node`, `Timeline`, shapes, `Text` / `MathExpr` / `CodeBlock`, `VoiceOver`, `KittenVoiceOverBackend`.
5. **Determinism** — avoid hidden globals; scene parameters (resolution, fps, seed) should be explicit or passed into `Scene`.

## Naming

- Module names: `snake_case` (`manimlite.core`).
- Public classes: `PascalCase` (`Circle`, `MathExpr`).
- Time in **seconds** as `float`.

## Anti-patterns (do not generate)

- LaTeX strings for math (use `MathExpr` + Typst syntax when implemented).
- Subclassing `Scene` with dozens of `play()` overrides unless the API explicitly documents it.
- Shelling out to `ffmpeg` for frame encoding (use PyAV pipeline when implemented).

## Example shape (conceptual)

```python
from manimlite import Scene, Circle, Timeline

scene = Scene(width=1920, height=1080, fps=30, duration=3.0)
# Nodes and timeline entries are added explicitly (API TBD in implementation).
_ = scene, Circle(radius=100.0), Timeline()
```

Refer to [docs/design/api-spec.md](docs/design/api-spec.md) for the authoritative public contract.
