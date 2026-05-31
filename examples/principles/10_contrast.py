"""Drawing principle: Contrast — value and scale.

Run: python examples/principles/10_contrast.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from motiongram import Scene, SkiaRenderer
from motiongram.export import PyAVEncoder

WIDTH, HEIGHT = 960, 540
FPS = 30.0
DURATION = 2.5
BG = (30, 30, 30)

from motiongram.shapes import Ellipse, Rectangle


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    scene.add_node(Rectangle(x=80, y=120, width=780, height=300, corner_radius=10.0, fill_color="#E8EAED", stroke_color="#B8BCC4", stroke_width=2.0))
    scene.add_node(Rectangle(x=140, y=190, width=220, height=160, corner_radius=12.0, fill_color="#2C2C2C", stroke_color="#1E1E1E", stroke_width=1.0))
    scene.add_node(Ellipse(x=620, y=260, rx=150, ry=150, fill_color="#A51C30", stroke_color="#FFFFFF", stroke_width=3.0))
    scene.add_node(Ellipse(x=780, y=400, rx=22, ry=22, fill_color="#5DD2E8", stroke_color="#FFFFFF", stroke_width=1.5))
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
