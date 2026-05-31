"""Gargantua-style black hole (Interstellar-inspired) — layered disk, spin, slow zoom.

This is a **stylized 2D composition**, not GR ray tracing: warm accretion bands, a dark
shadow, photon-ring stroke, and optional lensed hints. Motion comes from the timeline
(`Rotate`, `CameraZoom`) per AGENTS.md.

Run::

    python examples/recipes/interstellar_black_hole.py
    motiongram render examples/recipes/interstellar_black_hole.py -o gargantua.mp4

Requires: skia-python, PyAV.

"""

from __future__ import annotations

import math
import random
import sys
from pathlib import Path

from motiongram import CameraZoom, Rotate, Scene, SkiaRenderer
from motiongram.core import Node
from motiongram.export import PyAVEncoder
from motiongram.shapes import Arc, Ellipse, Line
from motiongram.value import GradientOverlay

WIDTH = 1280
HEIGHT = 720
FPS = 30.0
DURATION = 12.0

# Background RGB (also used as Skia clear); gradient sits on top.
BG = (8, 10, 22)

CX = WIDTH / 2.0
CY = HEIGHT / 2.0

# Full rotations of the accretion system over the clip
N_DISK_TURNS = 2.5

# Stylistic palette — warm disk on cold space
C_SPACE_LO = "#0A1628"
C_SPACE_HI = "#000000"


def _star_field() -> Node:
    rng = random.Random(2026)
    stars = Node(x=0.0, y=0.0)
    for _ in range(220):
        sx = rng.uniform(12.0, WIDTH - 12.0)
        sy = rng.uniform(12.0, HEIGHT - 12.0)
        # Avoid crowding the very center slightly
        if (sx - CX) ** 2 + (sy - CY) ** 2 < 140.0**2:
            continue
        r = rng.uniform(0.35, 2.1)
        tone = rng.choice(["#FFFFFF", "#E8ECFF", "#FFEEDD", "#D0E8FF"])
        stars.add(Ellipse(x=sx, y=sy, rx=r, ry=r, fill_color=tone, stroke_color=None, stroke_width=0.0))
    return stars


def _disk_and_hole() -> Node:
    """Subtree centered at origin; parent node placed at (CX, CY)."""
    g = Node(x=0.0, y=0.0)

    # Diffuse outer corona (very flat ellipse)
    g.add(
        Ellipse(
            x=0.0,
            y=0.0,
            rx=348.0,
            ry=56.0,
            fill_color="#CC4D0088",
            stroke_color=None,
            stroke_width=0.0,
        )
    )
    # "Lensed" duplicate — fainter band offset (artistic, not physical GR)
    g.add(
        Ellipse(
            x=0.0,
            y=-36.0,
            rx=300.0,
            ry=36.0,
            fill_color="#FFB84D55",
            stroke_color="#FFCC8833",
            stroke_width=1.5,
        )
    )
    # Main glowing accretion slab
    g.add(
        Ellipse(
            x=0.0,
            y=0.0,
            rx=302.0,
            ry=42.0,
            fill_color="#E85D0477",
            stroke_color="#FFAA0044",
            stroke_width=2.0,
        )
    )
    # Inner hot strip (thin bright band in the disk plane)
    g.add(
        Ellipse(
            x=0.0,
            y=0.0,
            rx=286.0,
            ry=11.0,
            fill_color="#FFFFFF55",
            stroke_color=None,
            stroke_width=0.0,
        )
    )
    # Faint circular arcs suggesting wrapped light (rotate with disk)
    g.add(
        Arc(
            x=0.0,
            y=0.0,
            radius=274.0,
            start_angle=math.pi * 0.05,
            end_angle=math.pi * 0.42,
            stroke_color="#FFD7A033",
            stroke_width=3.0,
        )
    )
    g.add(
        Arc(
            x=0.0,
            y=0.0,
            radius=274.0,
            start_angle=math.pi * 1.08,
            end_angle=math.pi * 1.45,
            stroke_color="#FFD7A033",
            stroke_width=3.0,
        )
    )

    # --- Black shadow & photon ring (on top of disk body) ---
    g.add(
        Ellipse(
            x=0.0,
            y=0.0,
            rx=76.0,
            ry=76.0,
            fill_color="#030203",
            stroke_color=None,
            stroke_width=0.0,
        )
    )
    g.add(
        Ellipse(
            x=0.0,
            y=0.0,
            rx=70.0,
            ry=70.0,
            fill_color="#00000000",
            stroke_color="#F9E7B0CC",
            stroke_width=2.6,
        )
    )
    g.add(
        Ellipse(
            x=0.0,
            y=0.0,
            rx=84.0,
            ry=84.0,
            fill_color="#00000000",
            stroke_color="#FFF5D633",
            stroke_width=1.2,
        )
    )

    # Cross-bar suggestion: thin orthogonal glint lines (very subtle)
    g.add(
        Line(
            x0=-110.0,
            y0=0.0,
            x1=110.0,
            y1=0.0,
            stroke_color="#FFFFFF18",
            stroke_width=1.0,
        )
    )
    return g


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)

    scene.add_node(
        GradientOverlay(
            x=0.0,
            y=0.0,
            width=float(WIDTH),
            height=float(HEIGHT),
            angle_rad=math.radians(128.0),
            stops=((0.0, C_SPACE_LO), (0.55, "#060D18"), (1.0, C_SPACE_HI)),
        )
    )
    scene.add_node(_star_field())

    disk_root = Node(x=CX, y=CY)
    disk_root.add(_disk_and_hole())
    scene.add_node(disk_root)

    scene.add_animation(
        0.0,
        DURATION,
        disk_root,
        Rotate(angle0=0.0, angle1=2.0 * math.pi * N_DISK_TURNS),
    )
    scene.add_animation(0.0, DURATION, scene.root, CameraZoom(scene, zoom0=1.0, zoom1=1.065))

    return scene


def get_skia_renderer() -> SkiaRenderer:
    return SkiaRenderer(clear_color=BG)


def main() -> None:
    scene = build_scene()
    out = Path(__file__).with_suffix(".mp4")
    encoder = PyAVEncoder(
        scene=scene,
        output_path=out,
        renderer=get_skia_renderer(),
        linear_timeline=True,
    )
    result = encoder.encode(verbose=True)
    print(f"Output: {result} ({result.stat().st_size:,} bytes)", file=sys.stderr)


if __name__ == "__main__":
    main()
