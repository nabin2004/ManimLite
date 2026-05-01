"""Drawing principle: Proportion — modular sizes & spacing.

Run: python examples/principles/07_proportion.py
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
BG = (15, 17, 26)

from manimlite.composition import PHI, distribute_evenly
from manimlite.shapes import RegularPolygon


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    nodes = []
    radii = (34.0, 34.0 * PHI, 34.0 * PHI * PHI)
    for r in radii:
        n = RegularPolygon(x=0, y=300, sides=6, radius=r, fill_color="#61AFEF", stroke_color="#24365A", stroke_width=1.5)
        scene.add_node(n)
        nodes.append(n)
    distribute_evenly(nodes, "x", 180.0, WIDTH - 180.0)
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
