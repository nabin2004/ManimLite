"""Drawing principle: Gesture — flowing rhythms.

Run: python examples/principles/12_gesture.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from typmotion import Scene, SkiaRenderer
from typmotion.export import PyAVEncoder

WIDTH, HEIGHT = 960, 540
FPS = 30.0
DURATION = 2.5
BG = (18, 14, 22)

from typmotion.composition import GesturePath


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    pts = ((-280, 120), (-120, 40), (40, -40), (220, -80), (420, 20), (620, 160))
    scene.add_node(GesturePath(x=WIDTH / 2, y=HEIGHT / 2 + 40, control_points=pts, stroke_color="#FF8B7B", stroke_width=5.0, taper=True))
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
