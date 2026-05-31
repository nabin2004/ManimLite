"""Drawing principle: Line — weight, dashes, Bézier.

Run: python examples/principles/01_line.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from motiongram import Scene, SkiaRenderer
from motiongram.export import PyAVEncoder

WIDTH, HEIGHT = 960, 540
FPS = 30.0
DURATION = 3.0
BG = (30, 30, 30)

from motiongram.shapes import BezierCurve, Line


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    thick = Line(x=80, y=420, x0=0, y0=0, x1=780, y1=0, stroke_color="#5DD2E8", stroke_width=6.0)
    dashed = Line(
        x=80, y=360, x0=0, y0=0, x1=720, y1=-120,
        stroke_color="#A51C30", stroke_width=3.0, dash_pattern=(18.0, 12.0),
    )
    bez = BezierCurve(
        x=120, y=280,
        p0=(0, 80), p1=(200, -40), p2=(520, 200), p3=(760, 20),
        stroke_color="#EDF1FA", stroke_width=3.5,
    )
    scene.add_node(thick)
    scene.add_node(dashed)
    scene.add_node(bez)
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
