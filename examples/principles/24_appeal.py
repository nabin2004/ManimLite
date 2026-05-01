"""Animation principle: Appeal — concise polished motion.

Run: python examples/principles/24_appeal.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from typmotion import Scene, SkiaRenderer
from typmotion.export import PyAVEncoder

WIDTH, HEIGHT = 960, 540
FPS = 30.0
DURATION = 3.0
BG = (14, 18, 28)

from typmotion import MoveY, Parallel, ScaleY
from typmotion.form import Sphere
from typmotion.shapes import Line
from typmotion.value import GradientOverlay


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    scene.add_node(GradientOverlay(x=0, y=0, width=float(WIDTH), height=float(HEIGHT), angle_rad=math.radians(95), stops=((0.0, "#1E2840"), (1.0, "#0E121C"))))
    scene.add_node(Line(x=120, y=120, x0=0, y0=0, x1=720, y1=0, stroke_color="#5DD2E8", stroke_width=4.0))
    hero = Sphere(x=520, y=300, radius=92.0)
    scene.add_node(hero)
    scene.add_animation(0.2, DURATION, hero, Parallel(MoveY(320.0, 280.0), ScaleY(sy0=0.92, sy1=1.06)))
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
