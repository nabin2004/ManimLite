"""Animation principle: Secondary action — layered motion.

Run: python examples/principles/20_secondary_action.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from motiongram import Scene, SkiaRenderer
from motiongram.export import PyAVEncoder

WIDTH, HEIGHT = 960, 540
FPS = 30.0
DURATION = 2.4
BG = (30, 30, 30)

from motiongram import MoveX, Parallel, Rotate
from motiongram.shapes import Rectangle


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    body = Rectangle(x=200, y=260, width=180, height=90, corner_radius=18.0, fill_color="#2C3A42", stroke_color="#FFFFFF", stroke_width=2.0)
    scene.add_node(body)
    scene.add_animation(
        0.0,
        DURATION,
        body,
        Parallel(MoveX(200.0, 680.0), Rotate(angle0=0.0, angle1=math.radians(8.0))),
    )
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
