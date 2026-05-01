"""Drawing principle: Value — gradients and shadow.

Run: python examples/principles/04_value.py
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
BG = (10, 12, 18)

from manimlite.form import Sphere
from manimlite.shapes import Rectangle
from manimlite.value import GradientOverlay, Shadow


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    scene.add_node(
        GradientOverlay(
            x=0,
            y=0,
            width=float(WIDTH),
            height=float(HEIGHT),
            angle_rad=math.radians(115),
            stops=((0.0, "#1E2537"), (1.0, "#0B0D12")),
        )
    )
    # Shadow shares the panel anchor so offset_x/y only nudge the silhouette down-right.
    panel_x, panel_y = 320.0, 180.0
    panel_w, panel_h = 260.0, 110.0
    scene.add_node(
        Shadow(
            x=panel_x,
            y=panel_y,
            width=panel_w,
            height=panel_h,
            offset_x=12.0,
            offset_y=14.0,
            corner_radius=16.0,
            color="#00000055",
        )
    )
    scene.add_node(
        Rectangle(
            x=panel_x,
            y=panel_y,
            width=panel_w,
            height=panel_h,
            corner_radius=16.0,
            fill_color="#2E3C56",
            stroke_color="#8FA3C4",
            stroke_width=1.5,
        )
    )
    scene.add_node(Sphere(x=520, y=280, radius=72.0))
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
