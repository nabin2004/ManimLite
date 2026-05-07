"""Drawing principle: Space — depth via scale, opacity, blur.

Run: python examples/principles/05_space.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from manimlite import Scene, SkiaRenderer
from manimlite.export import PyAVEncoder

WIDTH, HEIGHT = 960, 540
FPS = 30.0
DURATION = 3.0
BG = (30, 30, 30)

from manimlite import FadeIn, MoveX
from manimlite.shapes import Ellipse


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    far = Ellipse(x=480, y=280, rx=180, ry=110, fill_color="#333333", stroke_color=None, stroke_width=0.0)
    far.opacity = 0.35
    far.blur_sigma = 6.0
    mid = Ellipse(x=520, y=300, rx=120, ry=75, fill_color="#4A6B78", stroke_color="#B4B8BF", stroke_width=1.0)
    mid.opacity = 0.75
    near = Ellipse(x=580, y=330, rx=70, ry=48, fill_color="#A51C30", stroke_color="#FFFFFF", stroke_width=2.0)
    near.opacity = 1.0
    scene.add_node(far)
    scene.add_node(mid)
    scene.add_node(near)
    scene.add_animation(0.0, DURATION, far, MoveX(420.0, 460.0))
    scene.add_animation(0.0, DURATION, mid, MoveX(480.0, 520.0))
    scene.add_animation(0.0, DURATION, near, FadeIn(0.2, 1.0))
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
