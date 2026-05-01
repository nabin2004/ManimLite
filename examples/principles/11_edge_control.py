"""Drawing principle: Edge control — sharp vs soft (blur).

Run: python examples/principles/11_edge_control.py
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
BG = (16, 18, 26)

from manimlite import Blur
from manimlite.shapes import Ellipse


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    sharp = Ellipse(x=280, y=280, rx=120, ry=120, fill_color="#5DD2E8", stroke_color="#FFFFFF", stroke_width=3.0)
    soft = Ellipse(x=640, y=280, rx=120, ry=120, fill_color="#F0C060", stroke_color="#FFFFFF", stroke_width=3.0)
    scene.add_node(sharp)
    scene.add_node(soft)
    scene.add_animation(0.0, DURATION, soft, Blur(0.0, 10.0))
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
