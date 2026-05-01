"""Animation principle: Arcs vs linear translation.

Run: python examples/principles/19_arcs.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from manimlite import Scene, SkiaRenderer
from manimlite.export import PyAVEncoder

WIDTH, HEIGHT = 960, 540
FPS = 30.0
DURATION = 2.2
BG = (14, 16, 24)

from manimlite import MoveArc, MoveX
from manimlite.shapes import Ellipse


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    arc_ball = Ellipse(x=140, y=360, rx=40, ry=40, fill_color="#F0C060", stroke_color="#FFFFFF", stroke_width=2.0)
    line_ball = Ellipse(x=140, y=460, rx=40, ry=40, fill_color="#5DD2E8", stroke_color="#FFFFFF", stroke_width=2.0)
    scene.add_node(arc_ball)
    scene.add_node(line_ball)
    scene.add_animation(
        0.0,
        DURATION,
        arc_ball,
        MoveArc(x0=140.0, y0=360.0, x1=820.0, y1=360.0, arc_height=-140.0),
    )
    scene.add_animation(0.0, DURATION, line_ball, MoveX(140.0, 820.0))
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
