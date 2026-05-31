"""Principle: centered world units under a :class:`~motiongram.world.WorldPortal`.

Run::

    python examples/principles/26_world_viewport.py
    motiongram render examples/principles/26_world_viewport.py

The scene stacks many world-unit props (sky markers, hill, trees, grass, fence, orbs)
with timeline-driven drifting clouds and rain.  Procedural content is built from
:class:`~motiongram.procedural.RainyLandscapeManifest` in ``motiongram.procedural``.
Requires: skia-python.
"""

from __future__ import annotations

import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NamedTuple

from motiongram import (
    Scene,
    SkiaRenderer,
    WorldPortal,
    WorldSpec,
    place_on_ground,
    world_shell,
    world_to_screen,
)
from motiongram.core import Node
from motiongram.export import PyAVEncoder
from motiongram.procedural import (
    RainyLandscapeManifest,
    apply_rainy_landscape_animations,
    default_rainy_landscape_manifest,
    materialize_rainy_landscape,
    resting_anchor_y,
)
from motiongram.shapes import Ellipse, Rectangle

# ---------------------------------------------------------------------------
# Configuration (scene framing + principle hero disc — not part of manifest)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SceneConfig:
    width: int = 960
    height: int = 540
    fps: float = 30.0
    duration: float = 15.0
    bg_rgba: tuple[int, int, int, int] = (30, 30, 30, 255)
    letterbox_color: str = "#1E1E1E"


@dataclass(frozen=True)
class WorldConfig:
    width: float = 10.0
    ground_y: float = 2.5


@dataclass(frozen=True)
class DiscConfig:
    radius: float = 0.18
    fill: str = "#A51C30"
    stroke: str = "#C84A5C"
    stroke_width: float = 0.012


SCENE = SceneConfig()
WORLD = WorldConfig()
DISC = DiscConfig()
LAND_MANIFEST = default_rainy_landscape_manifest()

_ALPHA_WARN_THRESHOLD: int = 16


class ScreenPoint(NamedTuple):
    x: int
    y: int


def _clamp(value: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, value))


def _sample_alpha(frame: Any, row: int, col: int) -> int | None:
    shape = getattr(frame, "shape", None)
    if shape is None or len(shape) < 2:
        return None
    h, w = int(shape[0]), int(shape[1])
    row, col = _clamp(row, 0, h - 1), _clamp(col, 0, w - 1)
    channels = int(shape[2]) if len(shape) > 2 else 0
    if channels >= 4:
        return int(frame[row, col, 3])
    return 255 if channels >= 1 else None


def world_to_pixel(
    x: float,
    y: float,
    *,
    spec: WorldSpec,
    frame_w: int,
    frame_h: int,
) -> ScreenPoint:
    sx, sy = world_to_screen(x, y, spec=spec, frame_w=frame_w, frame_h=frame_h)
    return ScreenPoint(int(round(sx)), int(round(sy)))


def _build_scene_and_spec(
    cfg: SceneConfig = SCENE,
    world: WorldConfig = WORLD,
    landscape: RainyLandscapeManifest = LAND_MANIFEST,
) -> tuple[Scene, WorldSpec]:
    if cfg.width <= 0 or cfg.height <= 0:
        raise ValueError("width and height must be positive")

    scene = Scene(
        width=cfg.width,
        height=cfg.height,
        fps=cfg.fps,
        duration=cfg.duration,
    )
    scene.add_node(
        Rectangle(
            x=0.0,
            y=0.0,
            width=float(cfg.width),
            height=float(cfg.height),
            fill_color=cfg.letterbox_color,
        )
    )

    spec = WorldSpec(world_width=world.width, ground_y=world.ground_y)
    portal = WorldPortal(spec=spec, frame_width=cfg.width, frame_height=cfg.height)
    if portal.frame_width != scene.width or portal.frame_height != scene.height:
        raise ValueError("WorldPortal frame size must match Scene dimensions")

    shell = world_shell()
    portal.add(shell.world)
    scene.add_node(portal)

    handles = materialize_rainy_landscape(shell, spec, landscape)
    apply_rainy_landscape_animations(
        scene,
        duration=float(cfg.duration),
        manifest=landscape,
        handles=handles,
    )

    disc = Node(x=0.0, y=0.0)
    disc.add(
        Ellipse(
            x=0.0,
            y=0.0,
            rx=DISC.radius,
            ry=DISC.radius,
            fill_color=DISC.fill,
            stroke_color=DISC.stroke,
            stroke_width=DISC.stroke_width,
        )
    )
    place_on_ground(
        disc,
        resting_anchor_y(ground_y=spec.ground_y, radius_y=DISC.radius),
    )
    shell.midground.add(disc)

    return scene, spec


def build_scene() -> Scene:
    """CLI hook for ``motiongram render`` (must return :class:`~motiongram.core.Scene` only)."""
    scene, _ = _build_scene_and_spec()
    return scene


def _warn_faint_samples(
    frame: Any,
    samples: Iterable[tuple[int, int, str]],
) -> None:
    for row, col, tag in samples:
        alpha = _sample_alpha(frame, row, col)
        if alpha is not None and alpha < _ALPHA_WARN_THRESHOLD:
            print(
                f"warning: sample {tag!r} at ({row}, {col}) alpha={alpha} — check portal mapping",
                file=sys.stderr,
            )


def sanity_check_frame(
    rgba: Any,
    *,
    width: int,
    height: int,
    spec: WorldSpec,
) -> None:
    disc_cy = resting_anchor_y(ground_y=spec.ground_y, radius_y=DISC.radius)
    disc_px = world_to_pixel(0.0, disc_cy, spec=spec, frame_w=width, frame_h=height)
    ground_px = world_to_pixel(0.0, spec.ground_y, spec=spec, frame_w=width, frame_h=height)

    _warn_faint_samples(
        rgba,
        [
            (height // 2, width // 2, "frame_center"),
            (disc_px.y, disc_px.x, "disc_center"),
            (ground_px.y, ground_px.x, "ground_at_world_origin"),
        ],
    )


def get_renderer() -> SkiaRenderer:
    return SkiaRenderer(clear_color=SCENE.bg_rgba[:3])


def get_skia_renderer() -> SkiaRenderer:
    return get_renderer()


def main() -> None:
    scene, spec = _build_scene_and_spec()
    renderer = get_renderer()

    rgba = renderer.render_frame(scene, 0.0, ease=None)
    sanity_check_frame(rgba, width=scene.width, height=scene.height, spec=spec)

    out = Path(__file__).with_suffix(".mp4")
    encoder = PyAVEncoder(
        scene=scene,
        output_path=out,
        renderer=renderer,
        linear_timeline=True,
    )
    result = encoder.encode(verbose=True)
    print(f"Output: {result}", file=sys.stderr)


if __name__ == "__main__":
    main()
