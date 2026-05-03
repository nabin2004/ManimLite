"""Recipe: static world from primitive shapes (structure only, no timeline clips).

Hills, sun, and pine trees built from :class:`~manimlite.shapes.Rectangle`,
:class:`~manimlite.shapes.Ellipse`, :class:`~manimlite.shapes.Polygon`, and
:class:`~manimlite.shapes.Line`.

Run::

    python examples/recipes/spatial_landscape.py

Requires: skia-python.
"""

from __future__ import annotations

import sys
from pathlib import Path

from manimlite import Scene, SkiaRenderer
from manimlite.core import Node
from manimlite.export import PyAVEncoder
from manimlite.shapes import Ellipse, Line, Polygon, Rectangle

WIDTH, HEIGHT = 960, 540
FPS = 30.0
DURATION = 2.0
BG = (18, 22, 34)


def _pine_tree(x: float, y: float, *, scale: float = 1.0) -> Node:
    """Triangle foliage + brown trunk under a local ``Node``."""
    g = Node(x=x, y=y)
    s = scale
    foliage = Polygon(
        vertices=(
            (0.0, -90.0 * s),
            (-42.0 * s, 28.0 * s),
            (42.0 * s, 28.0 * s),
        ),
        fill_color="#3D7C47",
        stroke_color="#1F4026",
        stroke_width=1.5,
    )
    trunk = Rectangle(
        x=-10.0 * s,
        y=28.0 * s,
        width=20.0 * s,
        height=36.0 * s,
        corner_radius=3.0,
        fill_color="#6B4423",
        stroke_color="#3D2914",
        stroke_width=1.0,
    )
    g.add(trunk)
    g.add(foliage)
    return g


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)

    sky = Rectangle(x=0, y=0, width=float(WIDTH), height=float(HEIGHT), fill_color="#1E2538")
    scene.add_node(sky)

    hill = Polygon(
        vertices=((0.0, 420.0), (0.0, HEIGHT), (WIDTH, HEIGHT), (WIDTH, 340.0)),
        fill_color="#2C4C3E",
        stroke_color=None,
        stroke_width=0.0,
    )
    scene.add_node(hill)

    sun = Ellipse(
        x=780.0,
        y=120.0,
        rx=48.0,
        ry=48.0,
        fill_color="#F0C060",
        stroke_color="#FFD88A",
        stroke_width=2.0,
    )
    scene.add_node(sun)

    scene.add_node(_pine_tree(180.0, 380.0, scale=1.05))
    scene.add_node(_pine_tree(420.0, 400.0, scale=0.92))
    scene.add_node(_pine_tree(640.0, 388.0, scale=1.12))

    grass = Node(x=0, y=0)
    for i in range(28):
        gx = 36.0 + i * 34.0
        gy = float(HEIGHT - 28 - (i % 4) * 4)
        grass.add(
            Line(
                x0=gx,
                y0=gy,
                x1=gx + 8.0,
                y1=gy - 22.0 - (i % 3) * 5.0,
                stroke_color="#5FA86F",
                stroke_width=2.0,
            )
        )
    scene.add_node(grass)

    return scene


def get_skia_renderer() -> SkiaRenderer:
    return SkiaRenderer(clear_color=BG)


def main() -> None:
    scene = build_scene()
    out = Path(__file__).with_suffix(".mp4")
    encoder = PyAVEncoder(scene=scene, output_path=out, renderer=get_skia_renderer())
    result = encoder.encode(verbose=True)
    print(f"Output: {result}", file=sys.stderr)


if __name__ == "__main__":
    main()
