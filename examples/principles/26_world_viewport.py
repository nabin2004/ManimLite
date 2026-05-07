"""Principle: centered world units under a :class:`~manimlite.world.WorldPortal`.

Run::

    python examples/principles/26_world_viewport.py
    manimlite render examples/principles/26_world_viewport.py

The scene stacks many world-unit props (sky markers, hill, trees, grass, fence, orbs).
Requires: skia-python.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, NamedTuple

from manimlite import (
    Scene,
    SkiaRenderer,
    WorldPortal,
    WorldShellNodes,
    WorldSpec,
    ground_strip,
    place_on_ground,
    world_shell,
    world_to_screen,
)
from manimlite.core import Node
from manimlite.export import PyAVEncoder
from manimlite.shapes import Ellipse, Line, Polygon, Rectangle

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SceneConfig:
    width: int = 960
    height: int = 540
    fps: float = 30.0
    duration: float = 15.0
    # RGBA — 4 channels required by SkiaRenderer
    bg_rgba: tuple[int, int, int, int] = (30, 30, 30, 255)
    letterbox_color: str = "#1E1E1E"


@dataclass(frozen=True)
class WorldConfig:
    width: float = 10.0
    # y-down coordinate space: positive y maps downward on screen.
    # scale = frame_width / world_width = 960/10 = 96 px/unit
    # screen_y = frame_height/2 + ground_y*scale = 270 + 2.5*96 = 510 px ✓
    # Negative ground_y (the original -2.5) would place the ground 240 px
    # above centre — in the sky region.
    ground_y: float = 2.5
    ground_strip_thickness: float = 0.08
    ground_color: str = "#2E3230"


@dataclass(frozen=True)
class DiscConfig:
    radius: float = 0.18
    fill: str = "#A51C30"
    stroke: str = "#C84A5C"
    stroke_width: float = 0.012


SCENE = SceneConfig()
WORLD = WorldConfig()
DISC = DiscConfig()

_ALPHA_WARN_THRESHOLD: int = 16
_WORLD_HALF: float = WORLD.width / 2.0


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

class ScreenPoint(NamedTuple):
    x: int
    y: int


def resting_y(*, ground_y: float, radius_y: float) -> float:
    """World-space centre-y so the bottom of an ellipse sits exactly on *ground_y*.

    In ``WorldSpec``'s y-down space, the lowest point of an ellipse centred at
    ``cy`` is ``cy + radius_y``.  Setting that equal to *ground_y* gives
    ``cy = ground_y - radius_y`` — which places the centre *above* the ground
    line by one radius, as expected.

    Example with ground_y=2.5, radius=0.18 → centre at y=2.32, bottom at y=2.5 ✓
    """
    return ground_y - radius_y


def _clamp(value: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, value))


def _sample_alpha(frame: Any, row: int, col: int) -> int | None:
    """Return the alpha value of *frame* at (*row*, *col*), or ``None`` on error."""
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


# ---------------------------------------------------------------------------
# Node factory helpers
# ---------------------------------------------------------------------------

def _orb_on_ground(
    ground_y: float,
    *,
    x: float,
    radius: float,
    fill: str = DISC.fill,
    stroke: str = DISC.stroke,
    stroke_width: float = DISC.stroke_width,
) -> Node:
    node = Node(x=x, y=0.0)
    node.add(
        Ellipse(
            x=0.0, y=0.0,
            rx=radius, ry=radius,
            fill_color=fill,
            stroke_color=stroke,
            stroke_width=stroke_width,
        )
    )
    place_on_ground(node, resting_y(ground_y=ground_y, radius_y=radius))
    return node


def _pine_tree(x: float, ground_y: float, *, scale: float = 1.0) -> Node:
    s = scale
    trunk_h = 0.22 * s
    trunk_w = 0.06 * s

    root = Node(x=x, y=ground_y - trunk_h)
    root.add(
        Rectangle(
            x=-trunk_w / 2.0, y=0.0,
            width=trunk_w, height=trunk_h,
            corner_radius=0.01 * s,
            fill_color="#5A4A40",
            stroke_color="#3A3228",
            stroke_width=0.004,
        )
    )
    root.add(
        Polygon(
            vertices=(
                (0.0, -0.38 * s),
                (-0.22 * s, trunk_h * 0.98),
                (0.22 * s, trunk_h * 0.98),
            ),
            fill_color="#2A3830",
            stroke_color="#1A241F",
            stroke_width=0.006,
        )
    )
    return root


def _cloud(cx: float, cy: float) -> Node:
    _PUFFS = (
        (-0.16, 0.02, 0.12, 0.07),
        (0.0,   0.0,  0.15, 0.09),
        (0.15,  0.02, 0.11, 0.07),
    )
    group = Node(x=cx, y=cy)
    for ox, oy, rx, ry in _PUFFS:
        group.add(
            Ellipse(
                x=ox, y=oy, rx=rx, ry=ry,
                fill_color="#D0D4DC",
                stroke_color="#90949C",
                stroke_width=0.004,
            )
        )
    return group


# ---------------------------------------------------------------------------
# World population
# ---------------------------------------------------------------------------

def _add_stars(shell: WorldShellNodes) -> None:
    # Sky band: world y=0 (screen centre=270px) up to y≈-2.8 (screen top).
    # Stars are spread across y = -0.4 to -2.2 — comfortably inside.
    stars = Node(x=0.0, y=0.0)
    for i in range(28):
        sx = -_WORLD_HALF + 0.35 + (i % 7) * (WORLD.width / 6.5)
        sy = -0.4 - (i // 7) * 0.42 - (i % 3) * 0.09
        stars.add(
            Ellipse(
                x=sx, y=sy, rx=0.028, ry=0.028,
                fill_color="#E8EAED",
                stroke_color=None,
                stroke_width=0.0,
            )
        )
    shell.background.add(stars)


def _add_hill(shell: WorldShellNodes, gy: float) -> None:
    shell.background.add(
        Polygon(
            vertices=(
                (-_WORLD_HALF, gy + 0.85),
                (-_WORLD_HALF, gy - 0.02),
                (-1.35, gy - 0.38),
                (0.4,   gy - 0.52),
                (1.8,   gy - 0.35),
                (_WORLD_HALF, gy - 0.05),
                (_WORLD_HALF, gy + 0.85),
            ),
            fill_color="#262928",
            stroke_color=None,
            stroke_width=0.0,
        )
    )


def _add_ground(shell: WorldShellNodes, spec: WorldSpec) -> None:
    shell.background.add(
        ground_strip(
            spec,
            thickness=WORLD.ground_strip_thickness,
            fill_color=WORLD.ground_color,
        )
    )


def _add_sun_and_clouds(shell: WorldShellNodes) -> None:
    # Sun sits high in the sky — y=-2.0 maps to screen_y ≈ 270-192 = 78px
    sun = Node(x=3.55, y=-2.0)
    sun.add(
        Ellipse(
            x=0.0, y=0.0, rx=0.34, ry=0.34,
            fill_color="#C73E52",
            stroke_color="#6E2832",
            stroke_width=0.01,
        )
    )
    shell.midground.add(sun)

    # Clouds in the upper half of the sky band: y = -1.2 to -1.8
    _CLOUD_POSITIONS = ((-3.15, -1.4), (0.65, -1.2), (2.35, -1.7), (-0.85, -1.85))
    for cx, cy in _CLOUD_POSITIONS:
        shell.midground.add(_cloud(cx, cy))


def _add_trees(shell: WorldShellNodes, gy: float) -> None:
    _TREES = ((-3.75, 1.08), (-1.35, 0.92), (2.05, 1.02), (3.85, 1.14), (-0.15, 0.78))
    for tx, scale in _TREES:
        shell.midground.add(_pine_tree(tx, gy, scale=scale))


def _add_rocks(shell: WorldShellNodes, gy: float) -> None:
    _ROCKS = (
        (-4.0,  0.11, 0.06, "#5C5C6A"),
        (4.35,  0.09, 0.05, "#4A4A58"),
        (-2.85, 0.07, 0.04, "#6A6A78"),
        (1.15,  0.08, 0.05, "#50505E"),
    )
    for rx, rw, rh, fill in _ROCKS:
        rock = Node(x=rx, y=0.0)
        rock.add(
            Ellipse(
                x=0.0, y=0.0, rx=rw, ry=rh,
                fill_color=fill,
                stroke_color="#3A3A44",
                stroke_width=0.003,
            )
        )
        place_on_ground(rock, resting_y(ground_y=gy, radius_y=rh))
        shell.midground.add(rock)


def _add_grass(shell: WorldShellNodes, gy: float) -> None:
    grass = Node(x=0.0, y=0.0)
    for i in range(48):
        gx = -_WORLD_HALF + 0.12 + i * 0.21
        blade_len = 0.09 + (i % 5) * 0.018
        grass.add(
            Line(
                x0=gx, y0=gy,
                x1=gx + 0.035, y1=gy - blade_len,
                stroke_color="#4A6B78",
                stroke_width=0.007,
            )
        )
    shell.midground.add(grass)


def _add_fence(shell: WorldShellNodes, gy: float) -> None:
    fence = Node(x=0.0, y=0.0)
    for i in range(26):
        fx = -4.55 + i * 0.36
        fence.add(
            Rectangle(
                x=fx - 0.018, y=gy,
                width=0.036, height=0.3,
                corner_radius=0.004,
                fill_color="#6B6358",
                stroke_color="#4A4540",
                stroke_width=0.003,
            )
        )
    shell.midground.add(fence)


def _add_orbs(shell: WorldShellNodes, gy: float) -> None:
    _ORBS = (
        (-2.45, 0.09,  "#5DD2E8", "#3D9CAD"),
        (2.58,  0.075, "#C84A5C", "#A51C30"),
        (4.05,  0.055, "#454545", "#5DD2E8"),
    )
    for x, radius, fill, stroke in _ORBS:
        shell.midground.add(_orb_on_ground(gy, x=x, radius=radius, fill=fill, stroke=stroke))


def _add_birds(shell: WorldShellNodes) -> None:
    # Birds mid-sky: y=-0.8 to -1.1 → screen_y ≈ 270-77 to 270-106 px
    _BIRDS = ((-2.0, -0.9), (0.2, -1.1), (2.8, -0.8))
    birds = Node(x=0.0, y=0.0)
    for i, (bx, by) in enumerate(_BIRDS):
        birds.add(
            Ellipse(
                x=bx + 0.02 * i, y=by,
                rx=0.06, ry=0.025,
                fill_color="#3A3A3A",
                stroke_color=None,
                stroke_width=0.0,
            )
        )
    shell.foreground.add(birds)


def _populate_world(shell: WorldShellNodes, spec: WorldSpec) -> None:
    gy = float(spec.ground_y)

    _add_stars(shell)
    _add_hill(shell, gy)
    _add_ground(shell, spec)
    _add_sun_and_clouds(shell)
    _add_trees(shell, gy)
    _add_rocks(shell, gy)
    _add_grass(shell, gy)
    _add_fence(shell, gy)
    _add_orbs(shell, gy)
    _add_birds(shell)


# ---------------------------------------------------------------------------
# Scene assembly
# ---------------------------------------------------------------------------

def _build_scene_and_spec(
    cfg: SceneConfig = SCENE,
    world: WorldConfig = WORLD,
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
            x=0.0, y=0.0,
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

    _populate_world(shell, spec)

    # Main disc — rests on the ground at the world origin
    disc = Node(x=0.0, y=0.0)
    disc.add(
        Ellipse(
            x=0.0, y=0.0,
            rx=DISC.radius, ry=DISC.radius,
            fill_color=DISC.fill,
            stroke_color=DISC.stroke,
            stroke_width=DISC.stroke_width,
        )
    )
    place_on_ground(disc, resting_y(ground_y=spec.ground_y, radius_y=DISC.radius))
    shell.midground.add(disc)

    return scene, spec


def build_scene() -> Scene:
    """CLI hook for ``manimlite render`` (must return :class:`~manimlite.core.Scene` only)."""
    scene, _ = _build_scene_and_spec()
    return scene


# ---------------------------------------------------------------------------
# Sanity checks
# ---------------------------------------------------------------------------

def _warn_faint_samples(
    frame: Any,
    samples: Iterable[tuple[int, int, str]],
) -> None:
    for row, col, tag in samples:
        alpha = _sample_alpha(frame, row, col)
        if alpha is not None and alpha < _ALPHA_WARN_THRESHOLD:
            print(
                f"warning: sample {tag!r} at ({row}, {col}) alpha={alpha}"
                " — check portal mapping",
                file=sys.stderr,
            )


def sanity_check_frame(
    rgba: Any,
    *,
    width: int,
    height: int,
    spec: WorldSpec,
) -> None:
    """Spot-check key pixels: frame center, disc center, and ground origin."""
    disc_cy = resting_y(ground_y=spec.ground_y, radius_y=DISC.radius)
    disc_px = world_to_pixel(0.0, disc_cy, spec=spec, frame_w=width, frame_h=height)
    ground_px = world_to_pixel(0.0, spec.ground_y, spec=spec, frame_w=width, frame_h=height)

    _warn_faint_samples(
        rgba,
        [
            (height // 2, width // 2, "frame_center"),
            (disc_px.y,   disc_px.x,  "disc_center"),
            (ground_px.y, ground_px.x, "ground_at_world_origin"),
        ],
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def get_renderer() -> SkiaRenderer:
    return SkiaRenderer(clear_color=SCENE.bg_rgba[:3])


def get_skia_renderer() -> SkiaRenderer:
    """Hook for ``manimlite render`` — matches :func:`get_renderer`."""
    return get_renderer()


def main() -> None:
    scene, spec = _build_scene_and_spec()
    renderer = get_renderer()

    rgba = renderer.render_frame(scene, 0.0)
    sanity_check_frame(rgba, width=scene.width, height=scene.height, spec=spec)

    out = Path(__file__).with_suffix(".mp4")
    encoder = PyAVEncoder(scene=scene, output_path=out, renderer=renderer)
    result = encoder.encode(verbose=True)
    print(f"Output: {result}", file=sys.stderr)


if __name__ == "__main__":
    main()