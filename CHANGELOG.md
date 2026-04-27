# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Architecture notes in `AGENTS.md`:** three layers (structure / timeline / animators), timeline as the authority for motion over the clip, `Node.update` for non-spatial hooks only, anti-patterns (no motion in `update`, no drifting shape subclasses), and **`examples/play_circles.py`** as the canonical pattern.
- **`apply_timeline(..., on_apply=...)`:** optional callback after each successful `anim.apply` (signature includes global `t`, segment bounds, target, animator, `u_eased`) for tooling.
- **`Renderer(..., debug=True)`** and **`play(..., debug=True)`:** log each timeline application to **stderr** (animator type, segment, target id, `u`, and `x` / `progress` when present).
- **Timeline-driven animation:** `Scene.add_animation(start, end, target, animator)` appends to `scene.timeline`. `apply_timeline(scene, t, *, ease=smoothstep)` walks entries in order (skips `end <= start`); maps global `t` to segment-local `u ∈ [0, 1]`; passes `ease(u)` to `apply` (use `ease=None` for linear). `Renderer.render` applies the timeline at `t=0` before drawing. `Renderer.play` uses `n_frames = max(1, round(duration * fps))` and `t_frame = min(duration, (i + 1) * dt)` per frame, then `apply_timeline`, `root.update`, and `draw`.
- **`lerp`**, **`smoothstep`**, **`MoveX`**, **`CircleOutline`**, **`Animator`** (protocol): exported from `manimlite`. `CircleOutline` applies only to `Circle` (otherwise `TypeError`).
- **`Renderer.play(scene, *, realtime=True)`** and **`Node.update(t, dt)`:** non-positive `scene.fps` raises `ValueError`. Realtime playback clears the terminal each frame, paces with `sleep`, and hides/restores the cursor; `realtime=False` for tests and headless runs.
- **`examples/play_circles.py`:** declarative outline reveal (`CircleOutline`) and horizontal move (`MoveX`). **`examples/draw_circle.py`:** single-frame `render` with full circles by default.
- **Scene graph (terminal):** `Node` has `x`, `y`, `add()`, and `draw(canvas, ox, oy)` with parent-origin propagation; `Scene.add_node` delegates to `root.add()`.
- **`AsciiFrameCanvas`:** binds a `Renderer` and character grid so nodes call `set_pixel`.
- **`Circle`** (grid outline via polygon sampling in `core`); `manimlite.shapes.Circle` remains the Skia-oriented stub.
- Tests: timeline at `t=0`, `MoveX` end state, play/update, circle progress via `apply_timeline`, timeline debug stderr, scene graph rendering.

### Changed

- **`Circle.progress`:** outline fraction is no longer advanced automatically in `update`; drive it with `CircleOutline` / timeline or set it manually.
- **`Drawable`:** `draw` takes accumulated origin `ox`, `oy`.
- **`text` / `shapes` stubs:** `draw` matches `Node`; stubs call `Node.draw` for children.
- **`Circle.draw`:** uses `Node.draw(self, …)` instead of `super().draw` (slotted dataclass subclasses).
- **Voice-over:** Piper (`piper-tts`, GPL) replaced by **Kitten TTS** (Apache-2.0) behind the `[tts]` extra; default voice `Jasper`; default backend `KittenVoiceOverBackend`.
- **`learn/`:** 101 phase markdown files (`000`–`100`) from print renderer toward PyAV-oriented design.

### Added (earlier)

- Repository scaffold: `src/manimlite` package stubs, tests layout, CI skeleton.
- SDRE documentation: SRS, SDD, supporting design docs, ADRs, proposal, roadmap.
