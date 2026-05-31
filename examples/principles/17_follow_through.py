"""Animation principle: Follow-through — elastic settle.

Run: python examples/principles/17_follow_through.py
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

from motiongram import FollowThrough, MoveY
from motiongram.shapes import Ellipse


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    puck = Ellipse(x=480, y=160, rx=58, ry=58, fill_color="#5DD2E8", stroke_color="#FFFFFF", stroke_width=2.5)
    scene.add_node(puck)
    scene.add_animation(0.0, DURATION, puck, FollowThrough(MoveY(160.0, 360.0)))
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
