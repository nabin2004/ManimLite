# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **`Node.update(t, dt)`** and **`Renderer.play(scene)`:** time-stepped loop (`dt = 1 / scene.fps`, `frames = max(1, int(duration * fps))`) runs **update then draw** each frame via the same `AsciiFrameCanvas` / `root.draw` path as `render`. Non-positive `scene.fps` raises `ValueError`.
- **`examples/play_circles.py`:** `Renderer.play` with `DriftingCircle` (subclass) for horizontal motion; library **`Circle`** stays static unless you override `update`. **`examples/draw_circle.py`** is the single-frame `render` counterpart.
- Tests: `test_node_update_visits_self_and_children`, `test_play_calls_update_once_per_frame`, `test_play_rejects_non_positive_fps`.

- **Scene graph (terminal path):** `Node` now has `x`, `y`, and `add()`; `draw(canvas, ox, oy)` propagates parent origin so child positions are relative. `Scene.add_node` calls `root.add()`.
- **`AsciiFrameCanvas`** in `renderer.py`: binds a `Renderer` and frame so nodes call `set_pixel(x, y, ch)`. `Renderer.render` runs `scene.root.draw(canvas, 0, 0)` (replaces the old `_draw_node` walker).
- **`Circle`** in `core.py`: grid/outline circle via `set_pixel` (polygon sampling); exported from `manimlite`. Note: `manimlite.shapes.Circle` remains the separate Skia-oriented stub (`radius`, colors).
- Tests: `test_render_scene_draws_circle_node`, `test_render_propagates_parent_position`.

### Changed

- **`Drawable` protocol:** `draw` now takes optional `ox`, `oy` (accumulated world origin).
- **`text.py` / `shapes.py` stubs:** `draw` signatures aligned with `Node`; stubs call `Node.draw` so children still recurse.
- **`Circle.draw`:** uses `Node.draw(self, …)` instead of `super().draw` to avoid `TypeError` with chained `@dataclass(slots=True)` subclasses.

- `learn/` tutorial: 101 phase markdown files (`000`–`100`) building the engine concept from a print renderer to PyAV-oriented architecture.

### Changed

- Optional voice-over stack: **Piper** (`piper-tts`, GPL) replaced by **Kitten TTS** (Apache-2.0) behind the `[tts]` extra; default voice `Jasper`; default backend `KittenVoiceOverBackend`.

### Added (earlier)

- Repository scaffold: `src/manimlite` package stubs, tests layout, CI skeleton.
- SDRE documentation: SRS, SDD, supporting design docs, ADRs, proposal, roadmap.
