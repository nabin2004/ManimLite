"""Animation principle: Straight ahead vs pose-to-pose.

Run: python examples/principles/16_straight_pose.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from typmotion import Scene, SkiaRenderer
from typmotion.export import PyAVEncoder

WIDTH, HEIGHT = 960, 540
FPS = 30.0
DURATION = 2.6
BG = (14, 16, 24)

from typmotion import MoveX, Sequence
from typmotion.shapes import Ellipse


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    smooth = Ellipse(x=160, y=260, rx=48, ry=48, fill_color="#5DD2E8", stroke_color="#FFFFFF", stroke_width=2.0)
    stepped = Ellipse(x=160, y=380, rx=48, ry=48, fill_color="#F0C060", stroke_color="#FFFFFF", stroke_width=2.0)
    scene.add_node(smooth)
    scene.add_node(stepped)
    scene.add_animation(0.0, DURATION, smooth, MoveX(160.0, 780.0))
    scene.add_animation(
        0.0,
        DURATION,
        stepped,
        Sequence(MoveX(160.0, 360.0), MoveX(360.0, 560.0), MoveX(560.0, 780.0)),
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
