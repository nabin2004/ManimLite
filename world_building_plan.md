# World-building implementation plan (ManimLite)

This document describes **how** to grow ManimLite toward compositional “world” authoring—few primitives in combination, timeline-driven motion—and **what already exists** in the repo so new work stays aligned with [AGENTS.md](AGENTS.md).

For a short **lookup table** (shape ↔ example, animator ↔ principle demo), see [examples/WORLD_BUILDING.md](examples/WORLD_BUILDING.md). For the author-facing **approach** (coordinates, portal vs camera, ground, shells), see the [Approach](examples/WORLD_BUILDING.md#approach) section there.

---

## Vision

- **Spatial:** Build scenes from a small vocabulary of drawables grouped under [`Node`](src/manimlite/core.py): parent-relative coordinates, painter order, no hidden globals. Use [`manimlite.world`](src/manimlite/world.py) when coordinates should be **logical** (stage space) rather than pixels.
- **Temporal:** Schedule clips with [`Scene.add_animation`](src/manimlite/core.py) and compose behavior with leaf [`Animator`](src/manimlite/animate.py)s plus `Parallel`, `Sequence`, `Delay`, and principle-style wrappers—**not** ad hoc motion inside `Node.update` for layout.

Success looks like: reusable **recipes** (geometry factories + timeline helpers) that stay thin wrappers over the same public API authors already use in [examples/principles/](examples/principles/).

---

## What already supports us

### Architecture (normative)

Three layers from [AGENTS.md](AGENTS.md):

| Layer | Responsibility | Primary types |
|-------|----------------|---------------|
| Structure | Scene graph, poses, `draw` | `Node`, shapes under [`manimlite.shapes`](src/manimlite/shapes.py), [`manimlite.form`](src/manimlite/form.py), [`manimlite.world`](src/manimlite/world.py) |
| Time | When each animator runs | `Scene.timeline`, `add_animation`, `apply_timeline` |
| Behavior | How targets change over segment-local `t ∈ [0, 1]` | `MoveX`, `MoveY`, `SquashStretch`, `Parallel`, … |

This separation is the main guardrail: **visible change over the clip** should come from **timeline + animator**, with constructor poses as **setup**.

### Render pipeline (world → camera → Skia)

Intended flow for world-authored scenes:

1. **`WorldPortal`** maps a subtree whose `x` / `y` are world units into **frame pixel** coordinates using `SkiaCanvas.push_affine_2x3` (see [`render.py`](src/manimlite/render.py)).
2. **`SkiaRenderer.render_frame`** applies [`Scene.camera`](src/manimlite/core.py) (pan/zoom/rotate around the frame center) in **pixel** space, unchanged from before.
3. **`CameraPan` / `CameraZoom`** animate that pixel-space anchor; use them alongside a portal filling the raster (or derive pixel anchors with `world_to_screen` helpers when authoring).

Gravity / anchor / mirror stubs in `world.py` remain **explicitly unimplemented**: they raise `NotImplementedError` until bounds and copying are defined. Simulation-style integration must not replace timeline motion for ordinary clips.

### Drawing primitives (Skia-backed shapes)

Implemented under [`src/manimlite/shapes.py`](src/manimlite/shapes.py) and drawn via [`SkiaCanvas`](src/manimlite/render.py) helpers:

- **Strokes / paths:** `Line`, `BezierCurve`, `Arc`, `Path`
- **Fills:** `Polygon`, `Rectangle`, `Ellipse`, `RegularPolygon`
- **Circular wedges (filled):** `Sector`, `SemiCircle` — use [`fill_sector`](src/manimlite/render.py) on Skia; full-turn wedges delegate to ellipse fill.

[`examples/principles/25_shape_sectors.py`](examples/principles/25_shape_sectors.py) demonstrates wedges and a simple face; [`examples/recipes/animated_character.py`](examples/recipes/animated_character.py) uses semicircle eyes and a sector mouth.

### Composition patterns

- **`Node.add(...)`** — groups drawables; transforms propagate from parent anchor ([CHANGELOG.md](CHANGELOG.md), [AGENTS.md](AGENTS.md)).
- **World containers** — [`world_shell()`](src/manimlite/world.py) returns named nodes for background / mid / foreground and character/prop grouping; sibling order defines painter order (no automatic global sort on `world_z` in v1).
- **Approximate rings** — segment polylines with `Line` ([`examples/showcase_intro.py`](examples/showcase_intro.py) `_ring`).
- **Higher-level layout helpers** — [`manimlite.composition`](src/manimlite/composition.py) (`align`, `distribute_evenly`, `stack_vertical`, grids/spirals where applicable).

### Animation building blocks

- **Combinators:** `Parallel`, `Sequence`, `Delay` ([AGENTS.md](AGENTS.md)).
- **Principle demos:** [examples/principles/](examples/principles/) map Disney-style ideas to concrete animators (`SquashStretch`, `MoveArc`, `FadeOut`, `Anticipate`, …).

### Reusable timeline snippets (recipes layer)

[`src/manimlite/recipes.py`](src/manimlite/recipes.py) documents small helpers that **only** call `scene.add_animation`:

- `add_squash_stretch_drop` — mirrors the bouncing-ball pattern ([`examples/principles/13_squash_stretch.py`](examples/principles/13_squash_stretch.py)).
- `add_blink` — two-phase `ScaleY` on wrapper nodes (see [`examples/recipes/animated_character.py`](examples/recipes/animated_character.py)).

These are optional sugar; the semantic source of motion remains the principle examples and leaf animators.

### Procedural manifests (optional `manimlite.procedural`)

- **Purpose:** seedable, data-first descriptions (manifests) of parametrized worlds—terrain silhouettes, weather fields, discrete props—that **materialize** into [`world_shell()`](src/manimlite/world.py) buckets and return handles for wiring [`Scene.add_animation`](src/manimlite/core.py).
- **Not core engine:** authors import explicitly (`from manimlite.procedural import …`). Symbols are **not** re-exported from the `manimlite` package root so the stable public surface stays small.
- **Reference:** [`RainyLandscapeManifest`](src/manimlite/procedural/rainy_landscape.py) and [`examples/principles/26_world_viewport.py`](examples/principles/26_world_viewport.py).

### Compiler boundary (e.g. Manimator)

ManimLite is the **substrate**: `WorldSpec`, `WorldPortal`, the `Node` graph, discrete timeline entries (`start`, `end`, `target`, `Animator`). A higher-level toolchain (working name **Manimator**) should own narrative or curriculum intermediate representation—mapping pedagogical intent to manifests or directly to lowered scenes—and emit **fragments that compile to**:

- instantiated geometry under an existing portal/shell, and
- concrete `Animator` constructions passed to `add_animation`,

without growing topic logic inside [`manimlite.world`](src/manimlite/world.py), [`SkiaRenderer`](src/manimlite/render.py), or unrelated core modules.

### Starter scenes

| Goal | Example |
|------|---------|
| Spatial-only world sketch | [`examples/recipes/spatial_landscape.py`](examples/recipes/spatial_landscape.py) |
| Structure + clips + recipe helpers | [`examples/recipes/animated_character.py`](examples/recipes/animated_character.py) |
| Canonical timeline pattern | [`examples/play_circles.py`](examples/play_circles.py) |
| World portal + procedural manifest demo | [`examples/principles/26_world_viewport.py`](examples/principles/26_world_viewport.py) |

### Export and tooling

- **Video:** [`PyAVEncoder`](src/manimlite/export.py), [`SkiaRenderer`](src/manimlite/render.py).
- **Determinism / debug:** `Renderer(..., debug=True)` / `play(..., debug=True)` per [AGENTS.md](AGENTS.md).

---

## Implementation roadmap (phased)

The items below match the original world-building vision; **several are already done**—this section doubles as a checklist for future contributors.

### Phase A — Prove the vision in examples (mostly done)

- [x] Add `examples/recipes/` with at least one **spatial-only** scene and one scene using **timeline helpers** — see landscape + animated character recipes above.
- [ ] **Optional:** Extract repeated geometry (_ring_, dot grids) from [`showcase_intro.py`](examples/showcase_intro.py) into something like `examples/_geom_helpers.py` **when duplication hurts maintenance** (not required until multiple examples share the same helpers).

### Phase B — Shape primitives for circular segments (done)

- [x] Skia-backed filled wedges (`Sector`, `SemiCircle`) + principle-aligned demo [`25_shape_sectors.py`](examples/principles/25_shape_sectors.py).

### Phase C — Optional ergonomics (future)

- **Z-order:** Document painter order as default; add helpers only if backends expose ordering quirks or bugs ([dev_progress.md](dev_progress.md) learn items around grouping/z-order remain useful tutorials). Optional: global sort using `Node.world_z` behind a portal flag (not in v1).
- **Clipping / masks:** Consider only when UI-style worlds need hard edges (`ClipRect` / Skia clip ops)—depends on renderer API surface.

### Phase D — Rig pattern (document + exemplify)

- **Rig:** A `Node` subtree plus a small dataclass (or plain namespace) holding **references** to named child nodes; animations target those refs via `add_animation` **without** animators walking the scene graph ([AGENTS.md](AGENTS.md)).
- **Deliverable:** One short example or doc subsection showing `FaceRig(left_eye: Node, mouth: Node, …)` and clips attached to those handles.

### Phase E — World authoring (in progress / v1 landed)

- [x] **Centered world coordinates** — `WorldSpec`, `default_world_height`, `world_to_screen` / `screen_to_world`, `world_pixel_affine_coeffs`.
- [x] **Ground constant** — `WorldSpec.ground_y` + `DEFAULT_GROUND_Y` + `place_on_ground`.
- [x] **`WorldPortal`** — affine world → frame pixels via `SkiaCanvas.push_affine_2x3`; pair with `frame_width` / `frame_height` from the scene.
- [x] **Semantic shell** — `world_shell()`, `SemanticPart.role`, `CHARACTER_HEIGHT_UNITS` hint.
- [x] **Depth metadata** — `Node.world_z` (metadata only; no automatic reorder).
- [x] **Stubs** — `attach`, `mirror_x`, `apply_gravity_step` raise until bounds/simulation are defined; document timeline-first motion ([AGENTS.md](AGENTS.md)).
- [x] **Procedural manifest slice** — [`manimlite.procedural`](src/manimlite/procedural/__init__.py) (`RainyLandscapeManifest`, materialize + timeline helpers; see [26_world_viewport.py](examples/principles/26_world_viewport.py)).
- [ ] **Camera in world space** — optional future: `CameraPan` accepting `WorldSpec` or automatic conversion; today camera remains pixel-native after the portal.
- [ ] **Constraint / anchor system** — implement `attach` once parent bounds exist.

### Explicitly out of scope (near term)

- Boolean CSG (union/difference of fills), merged meshes—high cost; layered composition usually suffices for explainer-style illustrations.

---

## How to implement new world-building features

1. **Prefer factories over subclasses** — e.g. `def pine_tree(...) -> Node:` returning a configured subtree (same style as [`spatial_landscape.py`](examples/recipes/spatial_landscape.py)).
2. **Keep timeline helpers thin** — only `scene.add_animation(...)` (pattern in [`recipes.py`](src/manimlite/recipes.py)); avoid hiding targets or global clocks.
3. **New drawables** — add `@dataclass` nodes with `draw_world`, delegate to `Canvas`/`SkiaCanvas` methods; extend Skia backend when a primitive needs efficient support (as with `fill_sector`).
4. **New motion** — implement `Animator.apply(node, t)` on one target; compose with `Parallel`/`Sequence` rather than multi-target walks inside `apply`.
5. **Teach with links** — each new public helper should point to one principle demo or recipe so motion semantics stay discoverable ([WORLD_BUILDING.md](examples/WORLD_BUILDING.md)).

---

## Success criteria (recap)

- A newcomer can copy a **recipe** and build “eyes from two half-circles” in **~10 lines** of composition code (semicircles + parent `Node`).
- Principle demos remain the **meaning** of motion; recipes **reuse** the same animators.
- Scenes stay **deterministic**: explicit graph + explicit timeline, no parallel animation system in `Node.update` for ordinary motion.

---

## Related files

| Doc / code | Role |
|------------|------|
| [AGENTS.md](AGENTS.md) | Authoring rules, three-layer model, anti-patterns |
| [examples/WORLD_BUILDING.md](examples/WORLD_BUILDING.md) | Quick catalog, **Approach** section, world vs screen |
| [src/manimlite/world.py](src/manimlite/world.py) | World units, portal, authoring stubs |
| [src/manimlite/recipes.py](src/manimlite/recipes.py) | Timeline snippet helpers |
| [examples/recipes/](examples/recipes/) | compositional scene recipes |
