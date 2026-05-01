"""Drawing principle: Form — sphere, cube, cylinder.

Run: python examples/principles/03_form.py
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
BG = (12, 14, 22)

from typmotion.form import Cube, Cylinder, Sphere


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    scene.add_node(Sphere(x=220, y=280, radius=85.0))
    scene.add_node(Cube(x=500, y=300, size=160.0))
    scene.add_node(Cylinder(x=760, y=310, radius=70.0, height=130.0))
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
