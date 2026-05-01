"""Animation principle: Timing — same distance, different durations.

Run: python examples/principles/21_timing.py
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
BG = (14, 16, 24)

from manimlite import MoveX
from manimlite.shapes import Ellipse


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    fast = Ellipse(x=140, y=240, rx=46, ry=46, fill_color="#E06C75", stroke_color="#FFFFFF", stroke_width=2.0)
    slow = Ellipse(x=140, y=380, rx=46, ry=46, fill_color="#61AFEF", stroke_color="#FFFFFF", stroke_width=2.0)
    scene.add_node(fast)
    scene.add_node(slow)
    scene.add_animation(0.0, 1.0, fast, MoveX(140.0, 820.0))
    scene.add_animation(0.0, DURATION, slow, MoveX(140.0, 820.0))
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
