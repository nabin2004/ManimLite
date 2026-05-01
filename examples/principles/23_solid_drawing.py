"""Animation principle: Solid drawing — rotating form.

Run: python examples/principles/23_solid_drawing.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from manimlite import Scene, SkiaRenderer
from manimlite.export import PyAVEncoder

WIDTH, HEIGHT = 960, 540
FPS = 30.0
DURATION = 2.6
BG = (12, 14, 22)

from manimlite import Rotate
from manimlite.core import Node
from manimlite.form import Cube


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    grp = Node(x=480, y=300)
    grp.add(Cube(x=0, y=0, size=150.0))
    scene.add_node(grp)
    scene.add_animation(0.0, DURATION, grp, Rotate(angle0=0.0, angle1=math.radians(28.0)))
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
