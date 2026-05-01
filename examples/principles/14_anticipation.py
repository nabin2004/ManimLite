"""Animation principle: Anticipation — wind-up before motion.

Run: python examples/principles/14_anticipation.py
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
BG = (15, 17, 26)

from manimlite import Anticipate, MoveX
from manimlite.shapes import Rectangle


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    block = Rectangle(x=160, y=240, width=140, height=90, corner_radius=16.0, fill_color="#61AFEF", stroke_color="#FFFFFF", stroke_width=2.0)
    scene.add_node(block)
    scene.add_animation(0.0, DURATION, block, Anticipate(MoveX(160.0, 720.0), p1x=0.35, p1y=-0.12, p2x=0.65, p2y=1.02))
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
