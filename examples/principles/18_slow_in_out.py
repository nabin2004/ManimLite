"""Animation principle: Slow in & out — easing.

Run: python examples/principles/18_slow_in_out.py
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

from manimlite import MoveX, TimeScale
from manimlite.easing import ease_in_out_cubic
from manimlite.shapes import Ellipse


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    a = Ellipse(x=120, y=260, rx=44, ry=44, fill_color="#5DD2E8", stroke_color="#FFFFFF", stroke_width=2.0)
    b = Ellipse(x=120, y=380, rx=44, ry=44, fill_color="#A51C30", stroke_color="#FFFFFF", stroke_width=2.0)
    scene.add_node(a)
    scene.add_node(b)
    scene.add_animation(0.0, DURATION, a, MoveX(120.0, 820.0))
    scene.add_animation(0.0, DURATION, b, TimeScale(MoveX(120.0, 820.0), ease=ease_in_out_cubic))
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
