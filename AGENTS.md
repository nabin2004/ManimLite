# Agent / LLM authoring guide (ManimLite)

This file helps humans and **LLM agents** write scenes that match ManimLite’s intended public API.

## Design principles

1. **Flat over deep inheritance** — prefer `@dataclass` nodes and explicit composition over subclass trees.
2. **Explicit timelines** — animations are tuples `(start_time, end_time, target, animator)` attached to a scene, not implicit method call chains.
3. **Typed surfaces** — use type hints on public constructors and protocols (`Drawable`, `Animator`).
4. **Small vocabulary** — fewer top-level concepts than ManimCE: `Scene`, `Node`, `Timeline`, shapes, `Text` / `MathExpr` / `CodeBlock`, `VoiceOver`, `KittenVoiceOverBackend`.
5. **Determinism** — avoid hidden globals; scene parameters (resolution, fps, seed) should be explicit or passed into `Scene`.

## Architecture: three layers (normative)

ManimLite separates **structure**, **time scheduling**, and **how values change**. Keep these boundaries when generating scenes.

### Layer 1 — Structure (scene graph)

- **Types:** `Node`, `Circle`, text/shape stubs, etc.
- **Responsibility:** hierarchy (`children`, `add`), pose (`x`, `y`), and `draw(canvas, ox, oy)`.
- **No global scene clock** in this layer—nodes do not “know” the timeline.

### Layer 2 — Time (timeline)

- **Types:** `Scene.timeline`, `Scene.add_animation(start, end, target, animator)`.
- **Responsibility:** *when* an animator runs. Evaluation happens only through **`apply_timeline(scene, t, …)`** (used by `Renderer.render` at `t=0` and `Renderer.play` each frame). Use **`ease=None`** for linear easing (default is `smoothstep`).

### Layer 3 — Behavior (animators)

- **Types:** `MoveX`, `MoveY`, `CircleOutline`, and other `Animator` implementations (`apply(node, t)` with segment-local `t ∈ [0, 1]`).
- **Responsibility:** *how* the target changes. Animators should not walk the scene graph.

**Composition:** `Parallel(*animators)` runs every child with the same `t`. `Sequence(*animators)` splits `t ∈ [0, 1]` into equal slices and runs **one** child at a time—properties not written by the active child keep their prior values, so align segment boundaries when chaining. `Delay(animator, start, end)` runs the inner animator only when `start <= t <= end` (normalized within the parent segment); outside that range it does nothing (no “pin” to start—set initial pose on the node if needed).

**Rule of thumb:** any **visible change over the clip** should come from **timeline + animator**. Initial pose in a constructor (e.g. `Circle(…, progress=0.0)` so the first frame matches `CircleOutline` at `u=0` before the first `apply_timeline` step) is **setup**, not a second animation system.

**Canonical example:** [examples/play_circles.py](examples/play_circles.py) — outline via `CircleOutline`, translation via `MoveX`, no motion inside `Node.update` subclasses.

### `Node.update(t, dt)`

- Still run after `apply_timeline` in `play` for **recursion** and **non-spatial** logic (tests use a `CountingNode` pattern; future hooks might include simulation).
- **Do not** use `update` in user-facing scenes to mutate `x` / `y` / `progress` for motion—that bypasses the timeline and breaks determinism.

## Naming

- Module names: `snake_case` (`manimlite.core`).
- Public classes: `PascalCase` (`Circle`, `MathExpr`).
- Time in **seconds** as `float`.

## Anti-patterns (do not generate)

- LaTeX strings for math (use `MathExpr` + Typst syntax).
- Subclassing `Scene` with dozens of `play()` overrides unless the API explicitly documents it.
- Shelling out to `ffmpeg` for frame encoding (use **`PyAVEncoder`** / PyAV instead).
- **Motion inside `Node.update`** — do not move nodes by changing `x`, `y`, or `progress` in `update` for normal scenes; use **`add_animation`** + an **`Animator`**.
- **Geometry subclasses whose only job is motion** (e.g. a “drifting” `Circle` subclass with `x += speed * dt`) — use **`MoveX`** / other animators instead.
- Relying on **manual per-frame mutation** of drawable state outside **`apply_timeline`** for anything that should track scene time.

## Debugging

- Set **`Renderer(…, debug=True)`** or **`play(scene, debug=True)`** to log each timeline application to **stderr** (type of animator, target `id`, and snapshot of `x` / `progress` when present). Keeps **stdout** free for frame output.

## Example shape (conceptual)

```python
from manimlite import Scene, Circle, Timeline

scene = Scene(width=1920, height=1080, fps=30, duration=3.0)
# Nodes and timeline entries are added explicitly (API TBD in implementation).
_ = scene, Circle(radius=100.0), Timeline()
```

Refer to [docs/design/api-spec.md](docs/design/api-spec.md) for the authoritative public contract.
