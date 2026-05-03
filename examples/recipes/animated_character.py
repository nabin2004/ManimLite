"""Recipe: tiny character from combined primitives + shared timeline helpers.

Eyes use :class:`~manimlite.shapes.SemiCircle`; mouth is a :class:`~manimlite.shapes.Sector`.
Motion uses :func:`~manimlite.recipes.add_squash_stretch_drop` and
:func:`~manimlite.recipes.add_blink` (wrappers around ``add_animation``).

Run::

    python examples/recipes/animated_character.py

Requires: skia-python.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from manimlite import Scene, SkiaRenderer
from manimlite.core import Node
from manimlite.export import PyAVEncoder
from manimlite.recipes import add_blink, add_squash_stretch_drop
from manimlite.shapes import Ellipse, Rectangle, Sector, SemiCircle

WIDTH, HEIGHT = 960, 540
FPS = 30.0
DURATION = 2.8
BG = (14, 18, 28)


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)

    stage = Node(x=480.0, y=320.0)
    scene.add_node(stage)

    body = Ellipse(
        x=0.0,
        y=56.0,
        rx=72.0,
        ry=58.0,
        fill_color="#61AFEF",
        stroke_color="#24365A",
        stroke_width=2.5,
    )
    stage.add(body)

    face = Ellipse(
        x=0.0,
        y=-28.0,
        rx=95.0,
        ry=88.0,
        fill_color="#F5D4A8",
        stroke_color="#9B7356",
        stroke_width=2.0,
    )
    stage.add(face)

    left_eye = Node(x=-44.0, y=-38.0)
    left_eye.add(
        SemiCircle(
            x=0.0,
            y=0.0,
            radius=22.0,
            start_angle=math.pi,
            sweep_angle=math.pi,
            fill_color="#FFFFFF",
            stroke_color="#2E3440",
            stroke_width=2.0,
        )
    )
    left_pupil = Ellipse(x=0.0, y=4.0, rx=7.0, ry=9.0, fill_color="#2E3440")
    left_eye.add(left_pupil)

    right_eye = Node(x=44.0, y=-38.0)
    right_eye.add(
        SemiCircle(
            x=0.0,
            y=0.0,
            radius=22.0,
            start_angle=math.pi,
            sweep_angle=math.pi,
            fill_color="#FFFFFF",
            stroke_color="#2E3440",
            stroke_width=2.0,
        )
    )
    right_pupil = Ellipse(x=0.0, y=4.0, rx=7.0, ry=9.0, fill_color="#2E3440")
    right_eye.add(right_pupil)

    stage.add(left_eye)
    stage.add(right_eye)

    mouth = Sector(
        x=0.0,
        y=18.0,
        radius=46.0,
        start_angle=math.pi * 0.2,
        sweep_angle=math.pi * 0.6,
        fill_color="#C678DD",
        stroke_color="#5E3D6B",
        stroke_width=2.0,
    )
    stage.add(mouth)

    hat = Rectangle(
        x=-58.0,
        y=-118.0,
        width=116.0,
        height=28.0,
        corner_radius=6.0,
        fill_color="#E06C75",
        stroke_color="#8F3D46",
        stroke_width=2.0,
    )
    stage.add(hat)

    add_squash_stretch_drop(scene, stage, 0.0, DURATION, y0=320.0, y1=320.0, amount=0.28, axis="y")
    add_blink(scene, (left_eye, right_eye), 0.55, blink_duration=0.16, closed_scale_y=0.18)
    add_blink(scene, (left_eye, right_eye), 1.35, blink_duration=0.14, closed_scale_y=0.18)

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
