"""Animation principle: Exaggeration — pushed easing.

Run: python examples/principles/22_exaggeration.py
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
BG = (30, 30, 30)

from manimlite import ExaggerateEase, MoveX
from manimlite.shapes import Ellipse


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    plain = Ellipse(x=140, y=260, rx=42, ry=42, fill_color="#5DD2E8", stroke_color="#FFFFFF", stroke_width=2.0)
    pushed = Ellipse(x=140, y=400, rx=42, ry=42, fill_color="#A51C30", stroke_color="#FFFFFF", stroke_width=2.0)
    scene.add_node(plain)
    scene.add_node(pushed)
    scene.add_animation(0.0, DURATION, plain, MoveX(140.0, 820.0))
    scene.add_animation(0.0, DURATION, pushed, ExaggerateEase(MoveX(140.0, 820.0)))
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
