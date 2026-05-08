# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **PyAV export / render:** Optional `frames_dir` writes numbered PNG frames during encode; `PyAVEncoder(linear_timeline=…)` drives linear easing; `SkiaRenderer.render_frame(..., ease=…)` (default `smoothstep`). CLI: `manimlite render --frames-dir`.
- **Procedural presets (optional):** `manimlite.procedural` — `RainyLandscapeManifest`, `materialize_rainy_landscape`, `apply_rainy_landscape_animations` (seedable world content + timeline wiring; not re-exported from `manimlite`). Refactored `examples/principles/26_world_viewport.py` to consume the manifest; tests in `tests/test_procedural_rainy_landscape.py`.
- **World coordinates:** `manimlite.world` — `WorldSpec`, `WorldPortal`, `world_to_screen` / `screen_to_world`, `world_pixel_affine_coeffs`, light-weight shell helpers (`world_shell`, `ground_strip`, `place_on_ground`, …) and fake-depth projection (`project_depth_fake`); `SemanticPart` / `WorldShellNodes` for simple character-style rigs. Scene graph: `Node.world_z` for depth ordering alongside `x` / `y`.
- **Skia drawing:** `SkiaCanvas.fill_sector` (pie wedge) and `push_affine_2x3` / `pop_affine_2x3` for arbitrary 2×3 affines (used by world portal drawing).
- **Shapes:** `Sector` and `SemiCircle` in `manimlite.shapes` (Skia-backed wedge fill via `fill_sector`).
- **Timeline recipes:** `manimlite.recipes` — `add_blink`, `add_squash_stretch_drop` as thin wrappers over `Scene.add_animation`.
- **Tests:** `tests/test_world_projection.py` (world ↔ pixel mapping, affine consistency, camera zoom).
- **Examples:** `examples/WORLD_BUILDING.md`; `examples/principles/25_shape_sectors.py`, `26_world_viewport.py`; `examples/recipes/animated_character.py`, `spatial_landscape.py`; `examples/mlp_slides_typst.py`.
- **README demo:** tracked `docs/assets/readme-demo.mp4` (720p showcase) with a `.gitignore` exception for `docs/assets/**/*.mp4`; README embeds the clip for GitHub viewers.
- **Docs:** `docs/guides/principles-examples.md` indexes `examples/principles/` (drawing 01–12, animation 13–24); `docs/assets/README.md` explains checked-in media.
- **Principles examples:** `examples/principles/*.py` gallery (referenced from README and setup guide).
- **Skia text and code:** `SkiaCanvas.draw_text`; `Text.draw` draws labels on Skia; `CodeBlock.draw` uses Pygments token colors and monospace `draw_text` per character.
- **Video export:** `PyAVEncoder(scene, output_path, renderer=…).encode()` streams frames from `SkiaRenderer` into an H.264 **MP4** via PyAV (RGB pad to even dimensions, `libx264`, `yuv420p`).
- **CLI:** `manimlite render <scene.py> [-o OUT] [--width …] [--height …] [--fps …] [-q]` loads `build_scene()` or module `scene`, optional **`get_skia_renderer()`** hook for custom `SkiaRenderer(clear_color=…)`.
- **Animator:** `MoveY(y0, y1)` (symmetric with `MoveX`); exported from `manimlite`.
- **Public exports:** `PyAVEncoder`, `MoveY` in `manimlite.__all__`.
- **Examples:** `examples/showcase_intro.py` (720p reel), `examples/math_and_text.py`, `examples/check_skia_typst.py` (pipeline smoke check), `examples/engine_step.py`, `examples/showcase_play_circles.py`.
- **Docs:** `docs/guides/setup.md`, `docs/guides/math-rendering.md`, `docs/guides/principles-examples.md`; README quick start for Skia/Typst/PyAV path.
- **Tests:** `tests/unit/test_text_code_export.py` (Text, CodeBlock, encoder, `draw_text`); `MoveX`+`MoveY` parallel test.
- **`shapes.Line`:** docstring — use **keyword** args for `x0`…`y1`; positional args bind `Node` `x`, `y`, `children` first.
- **Architecture notes in `AGENTS.md`:** three layers (structure / timeline / animators), timeline as the authority for motion over the clip, `Node.update` for non-spatial hooks only, anti-patterns (no motion in `update`, no drifting shape subclasses), and **`examples/play_circles.py`** as the canonical pattern.
- **`apply_timeline(..., on_apply=...)`:** optional callback after each successful `anim.apply` (signature includes global `t`, segment bounds, target, animator, `u_eased`) for tooling.
- **`Renderer(..., debug=True)`** and **`play(..., debug=True)`:** log each timeline application to **stderr** (animator type, segment, target id, `u`, and `x` / `progress` when present).
- **Timeline-driven animation:** `Scene.add_animation(start, end, target, animator)` appends to `scene.timeline`. `apply_timeline(scene, t, *, ease=smoothstep)` walks entries in order (skips `end <= start`); maps global `t` to segment-local `u ∈ [0, 1]`; passes `ease(u)` to `apply` (use `ease=None` for linear). `Renderer.render` applies the timeline at `t=0` before drawing. `Renderer.play` uses `n_frames = max(1, round(duration * fps))` and `t_frame = min(duration, (i + 1) * dt)` per frame, then `apply_timeline`, `root.update`, and `draw`.
- **`lerp`**, **`smoothstep`**, **`MoveX`**, **`CircleOutline`**, **`Animator`** (protocol): exported from `manimlite`. `CircleOutline` applies only to `Circle` (otherwise `TypeError`).
- **Composable animators:** **`Parallel(*animators)`** (same `t` to each child), **`Sequence(*animators)`** (equal time slices, one child active), **`Delay(animator, start, end)`** (inner `apply` only when `start <= t <= end` within the parent segment, `0 <= start < end <= 1`). Documented in `AGENTS.md`.
- **`Renderer.play(scene, *, realtime=True)`** and **`Node.update(t, dt)`:** non-positive `scene.fps` raises `ValueError`. Realtime playback clears the terminal each frame, paces with `sleep`, and hides/restores the cursor; `realtime=False` for tests and headless runs.
- **`examples/play_circles.py`:** declarative outline reveal (`CircleOutline`) and horizontal move (`MoveX`). **`examples/draw_circle.py`:** single-frame `render` with full circles by default.
- **Scene graph (terminal):** `Node` has `x`, `y`, `add()`, and `draw(canvas, ox, oy)` with parent-origin propagation; `Scene.add_node` delegates to `root.add()`.
- **`AsciiFrameCanvas`:** binds a `Renderer` and character grid so nodes call `set_pixel`.
- **`Circle`** (grid outline via polygon sampling in `core`); `manimlite.shapes.Circle` remains the Skia-oriented stub.
- Tests: timeline at `t=0`, `MoveX` end state, play/update, circle progress via `apply_timeline`, timeline debug stderr, composable animators (`tests/unit/test_compose.py`), scene graph rendering.

### Changed

- **Branding:** Restored **ManimLite** as the project name and **`manimlite`** as the Python package / CLI (the **Typmotion** rename was reverted).
- **Camera defaults:** when `Camera.x` / `Camera.y` are unset (`nan`), the Skia renderer pins the viewport center to the **scene** center so world `(0, 0)` aligns with the top-left of the scene.
- **Export / CLI:** `PyAVEncoder.encode` and `manimlite render` are implemented (previously stubs).
- **`Circle.progress`:** outline fraction is no longer advanced automatically in `update`; drive it with `CircleOutline` / timeline or set it manually.
- **`Drawable`:** `draw` takes accumulated origin `ox`, `oy`.
- **`text` / `shapes` stubs:** `draw` matches `Node`; stubs call `Node.draw` for children.
- **`Circle.draw`:** uses `Node.draw(self, …)` instead of `super().draw` (slotted dataclass subclasses).
- **Voice-over:** Piper (`piper-tts`, GPL) replaced by **Kitten TTS** (Apache-2.0) behind the `[tts]` extra; default voice `Jasper`; default backend `KittenVoiceOverBackend`.
- **`learn/`:** 101 phase markdown files (`000`–`100`) from print renderer toward PyAV-oriented design.

### Fixed

- **Skia:** `GradientShader.MakeLinear` uses a **sequence** of two endpoints `(Point, Point)` for current skia-python bindings.

### Added (earlier)

- Repository scaffold: `src/manimlite` package stubs, tests layout, CI skeleton.
- SDRE documentation: SRS, SDD, supporting design docs, ADRs, proposal, roadmap.
