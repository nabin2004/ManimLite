"""Drawing principle: Perspective — grid + blocks.

Run: python examples/principles/06_perspective.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from manimlite import Scene, SkiaRenderer
from manimlite.export import PyAVEncoder

WIDTH, HEIGHT = 960, 540
FPS = 30.0
DURATION = 2.5
BG = (30, 30, 30)

from manimlite.perspective import PerspectiveGrid
from manimlite.shapes import Polygon


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    scene.add_node(PerspectiveGrid(x=0, y=0, width=float(WIDTH), height=float(HEIGHT), vanishing_x=WIDTH * 0.52, horizon_y=HEIGHT * 0.42))
    scene.add_node(Polygon(x=420, y=420, vertices=((0, 0), (90, -30), (110, 140), (-20, 160)), fill_color="#2C3A42", stroke_color="#5DD2E8", stroke_width=1.5))
    scene.add_node(Polygon(x=560, y=400, vertices=((0, 0), (70, -25), (85, 120), (-15, 135)), fill_color="#A51C30", stroke_color="#C84A5C", stroke_width=1.5))
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
