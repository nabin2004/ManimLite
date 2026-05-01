"""Drawing principle: Shape — primitives.

Run: python examples/principles/02_shape.py
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
BG = (14, 18, 28)

from typmotion.shapes import Ellipse, Rectangle, RegularPolygon


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    scene.add_node(Rectangle(x=120, y=160, width=220, height=140, corner_radius=18.0, fill_color="#3F6CAC", stroke_color="#7CADFF", stroke_width=2.0))
    scene.add_node(Ellipse(x=520, y=240, rx=110, ry=70, fill_color="#E06C75", stroke_color="#FFFFFF", stroke_width=2.0))
    scene.add_node(RegularPolygon(x=780, y=260, sides=5, radius=90.0, phase=-math.pi / 2, fill_color="#61AFEF", stroke_color="#24365A", stroke_width=2.0))
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
