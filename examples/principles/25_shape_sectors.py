"""Drawing principle: Shape — circular sectors and semicircles.

Demonstrates :class:`~manimlite.shapes.Sector` / :class:`~manimlite.shapes.SemiCircle`
for filled wedges (eyes, pie slices) without hand-tessellating polygons.

Run::

    python examples/principles/25_shape_sectors.py

Requires: skia-python.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from manimlite import Scene, SkiaRenderer
from manimlite.core import Node
from manimlite.export import PyAVEncoder
from manimlite.shapes import Ellipse, Sector, SemiCircle

WIDTH, HEIGHT = 960, 540
FPS = 30.0
DURATION = 2.2
BG = (30, 30, 30)


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)

    pie = Sector(x=240.0, y=280.0, radius=90.0, start_angle=-math.pi / 4, sweep_angle=math.pi * 1.25, fill_color="#5DD2E8", stroke_color="#3D3D3D", stroke_width=2.5)
    scene.add_node(pie)

    face = Node(x=620.0, y=260.0)
    face_base = Ellipse(x=0.0, y=0.0, rx=100.0, ry=92.0, fill_color="#D4CCC4", stroke_color="#6E5A50", stroke_width=2.0)
    face.add(face_base)

    face.add(
        SemiCircle(
            x=-46.0,
            y=-28.0,
            radius=24.0,
            start_angle=math.pi,
            sweep_angle=math.pi,
            fill_color="#FFFFFF",
            stroke_color="#3D3D3D",
            stroke_width=2.0,
        )
    )
    face.add(
        SemiCircle(
            x=46.0,
            y=-28.0,
            radius=24.0,
            start_angle=math.pi,
            sweep_angle=math.pi,
            fill_color="#FFFFFF",
            stroke_color="#3D3D3D",
            stroke_width=2.0,
        )
    )
    face.add(Sector(x=0.0, y=28.0, radius=38.0, start_angle=math.pi * 0.25, sweep_angle=math.pi * 0.55, fill_color="#A51C30", stroke_color="#6E2832", stroke_width=2.0))
    scene.add_node(face)

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
