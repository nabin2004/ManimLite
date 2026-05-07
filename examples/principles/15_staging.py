"""Animation principle: Staging — camera zoom isolates subject.

Run: python examples/principles/15_staging.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from manimlite import Scene, SkiaRenderer
from manimlite.export import PyAVEncoder

WIDTH, HEIGHT = 960, 540
FPS = 30.0
DURATION = 3.0
BG = (30, 30, 30)

from manimlite import CameraZoom, FadeOut
from manimlite.core import Node
from manimlite.shapes import Ellipse, Rectangle


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    bg = Node()
    for _, (dx, col) in enumerate([(0, "#2A2A2A"), (140, "#333333"), (280, "#3D3D3D")]):
        bg.add(Rectangle(x=120.0 + dx, y=180.0, width=110.0, height=220.0, corner_radius=14.0, fill_color=col, stroke_color="#4A4A4A", stroke_width=1.0))
    hero = Ellipse(x=480, y=300, rx=95, ry=95, fill_color="#A51C30", stroke_color="#FFFFFF", stroke_width=3.0)
    scene.add_node(bg)
    scene.add_node(hero)
    scene.add_animation(0.4, DURATION, bg.children[0], FadeOut(start=1.0, end=0.12))
    scene.add_animation(0.4, DURATION, bg.children[1], FadeOut(start=1.0, end=0.12))
    scene.add_animation(0.4, DURATION, bg.children[2], FadeOut(start=1.0, end=0.12))
    scene.add_animation(0.0, DURATION, scene.root, CameraZoom(scene, zoom0=1.0, zoom1=1.45))
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
