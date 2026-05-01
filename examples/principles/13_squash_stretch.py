"""Animation principle: Squash & stretch — bouncing ball.

Run: python examples/principles/13_squash_stretch.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from typmotion import Scene, SkiaRenderer
from typmotion.export import PyAVEncoder

WIDTH, HEIGHT = 960, 540
FPS = 30.0
DURATION = 2.4
BG = (14, 16, 24)

from typmotion import MoveY, Parallel, SquashStretch
from typmotion.core import Node
from typmotion.shapes import Ellipse


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    group = Node(x=480, y=120)
    ball = Ellipse(x=0, y=0, rx=56, ry=56, fill_color="#F0C060", stroke_color="#FFFFFF", stroke_width=2.0)
    group.add(ball)
    scene.add_node(group)
    scene.add_animation(0.0, DURATION, group, Parallel(SquashStretch(amount=0.45, axis="y"), MoveY(120.0, 380.0)))
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
