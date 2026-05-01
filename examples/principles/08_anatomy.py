"""Drawing principle: Anatomy — simple jointed figure.

Run: python examples/principles/08_anatomy.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from typmotion import Scene, SkiaRenderer
from typmotion.export import PyAVEncoder

WIDTH, HEIGHT = 960, 540
FPS = 30.0
DURATION = 2.5
BG = (18, 20, 30)

from typmotion.shapes import Line, Polygon


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    cx, cy = WIDTH / 2, HEIGHT / 2 - 40
    scene.add_node(Line(x=cx, y=cy - 120, x0=0, y0=0, x1=0, y1=-70, stroke_color="#EDF1FA", stroke_width=4.0))  # neck
    scene.add_node(Line(x=cx, y=cy - 40, x0=0, y0=0, x1=-70, y1=90, stroke_color="#EDF1FA", stroke_width=4.0))  # arm L
    scene.add_node(Line(x=cx, y=cy - 40, x0=0, y0=0, x1=70, y1=90, stroke_color="#EDF1FA", stroke_width=4.0))  # arm R
    scene.add_node(Line(x=cx, y=cy + 40, x0=0, y0=0, x1=-40, y1=140, stroke_color="#EDF1FA", stroke_width=5.0))  # leg L
    scene.add_node(Line(x=cx, y=cy + 40, x0=0, y0=0, x1=40, y1=140, stroke_color="#EDF1FA", stroke_width=5.0))  # leg R
    scene.add_node(Polygon(x=cx, y=cy - 150, vertices=((-22, -18), (22, -18), (26, 28), (-26, 28)), fill_color="#F0C060", stroke_color="#8B6914", stroke_width=2.0))
    scene.add_node(Polygon(x=cx, y=cy, vertices=((-36, -44), (36, -44), (42, 88), (-42, 88)), fill_color="#5DD2E8", stroke_color="#2E6F80", stroke_width=2.5))
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
