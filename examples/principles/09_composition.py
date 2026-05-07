"""Drawing principle: Composition — rule of thirds + golden spiral.

Run: python examples/principles/09_composition.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from manimlite import Scene, SkiaRenderer
from manimlite.export import PyAVEncoder

WIDTH, HEIGHT = 960, 540
FPS = 30.0
DURATION = 2.5
BG = (30, 30, 30)

from manimlite.composition import GoldenSpiral, RuleOfThirdsGrid
from manimlite.shapes import Ellipse


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    scene.add_node(RuleOfThirdsGrid(width=float(WIDTH), height=float(HEIGHT)))
    scene.add_node(GoldenSpiral(x=WIDTH * 0.62, y=HEIGHT * 0.58, loops=2.4, a=4.0, b=0.22))
    scene.add_node(Ellipse(x=WIDTH / 3, y=HEIGHT / 3, rx=46, ry=46, fill_color="#A51C30", stroke_color="#FFFFFF", stroke_width=2.0))
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
