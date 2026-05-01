"""Polished intro reel — richer geometry, two-tone accents, choreographed timing.

Dark "editor" palette, 3-act animation structure, layered ring geometry,
diagonal slash, dot-grid atmosphere, and a floating glyph that breathes.

Run::

    python examples/showcase_intro.py
    manimlite render examples/showcase_intro.py -o showcase.mp4

Requires: skia-python, ``typst`` on ``PATH``.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from manimlite import MoveX, MoveY, Parallel, Scene, SkiaRenderer
from manimlite.export import PyAVEncoder
from manimlite.core import Node
from manimlite.shapes import Line, Polygon
from manimlite.text import CodeBlock, MathExpr, Text

# ---------------------------------------------------------------------------
# Layout constants
# ---------------------------------------------------------------------------

WIDTH = 1280
HEIGHT = 720
FPS = 30.0
DURATION = 11.0          # Extended slightly so the final breath has room

# Palette — two distinct accent hues to create hierarchy
BG          = (14, 18, 28)      # Deeper navy-black (not pure black)

C_ACCENT_COOL = "#5DD2E8"       # Cyan  — UI bar, rule, rings
C_ACCENT_WARM = "#F0C060"       # Gold  — glyph, hex, outer ring
C_TITLE       = "#EDF1FA"
C_MUTED       = "#8FA3C4"
C_TAGLINE     = "#5E7291"
C_CODE_BG     = "#1E2537"
C_PANEL_EDGE  = "#2E3C56"
C_DOT         = "#2A3550"       # Atmosphere dots


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ring(
    node: Node,
    radius: float,
    segments: int,
    *,
    color: str,
    width: float,
    phase: float = 0.0,
) -> None:
    """Approximate a circle with ``Line`` segments (crisp on Skia).

    ``phase`` rotates the entire ring by that many radians — useful for
    counter-rotating decorative rings.
    """
    for i in range(segments):
        a0 = phase + 2 * math.pi * i / segments
        a1 = phase + 2 * math.pi * (i + 1) / segments
        node.add(
            Line(
                x0=radius * math.cos(a0),
                y0=radius * math.sin(a0),
                x1=radius * math.cos(a1),
                y1=radius * math.sin(a1),
                stroke_color=color,
                stroke_width=width,
            )
        )


def _hexagon(radius: float, phase: float = 0.0) -> tuple[tuple[float, float], ...]:
    return tuple(
        (
            radius * math.cos(phase + math.pi / 3 * k),
            radius * math.sin(phase + math.pi / 3 * k),
        )
        for k in range(6)
    )


def _dot_grid(
    node: Node,
    cols: int,
    rows: int,
    spacing: float,
    *,
    color: str,
    size: float = 2.0,
) -> None:
    """Add a grid of small square dots for atmospheric depth."""
    ox = -(cols - 1) * spacing / 2
    oy = -(rows - 1) * spacing / 2
    for r in range(rows):
        for c in range(cols):
            x = ox + c * spacing
            y = oy + r * spacing
            node.add(
                Polygon(
                    vertices=(
                        (x - size, y - size),
                        (x + size, y - size),
                        (x + size, y + size),
                        (x - size, y + size),
                    ),
                    fill_color=color,
                    stroke_color=color,
                    stroke_width=0.0,
                )
            )


def _diagonal_slash(
    node: Node,
    *,
    color: str,
    width: float,
) -> None:
    """Single angled line that cuts diagonally — asymmetric compositional anchor."""
    node.add(
        Line(
            x0=780.0, y0=60.0,
            x1=920.0, y1=660.0,
            stroke_color=color,
            stroke_width=width,
        )
    )


# ---------------------------------------------------------------------------
# Scene assembly
# ---------------------------------------------------------------------------

def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)

    # -----------------------------------------------------------------------
    # ACT 1 (t = 0.0 – 2.5): Geometry arrives — stage is set
    # -----------------------------------------------------------------------

    # Atmosphere: dot grid (static, fades in from right with panel)
    dots = Node(x=960.0, y=360.0)
    _dot_grid(dots, cols=9, rows=7, spacing=38.0, color=C_DOT, size=1.8)
    scene.add_node(dots)
    scene.add_animation(0.0, 1.4, dots, MoveX(1100.0, 960.0))

    # Diagonal slash — arrives early, anchors the right half
    slash = Node(x=0.0, y=0.0)
    _diagonal_slash(slash, color="#29364F", width=2.5)
    scene.add_node(slash)
    scene.add_animation(0.1, 1.0, slash, MoveY(-80.0, 0.0))

    # Left panel background
    panel = Node(x=0.0, y=0.0)
    panel.add(
        Polygon(
            vertices=((36.0, 80.0), (755.0, 72.0), (742.0, 640.0), (28.0, 648.0)),
            fill_color=C_CODE_BG,
            stroke_color=C_PANEL_EDGE,
            stroke_width=1.5,
        )
    )
    # Inner glow overlay: slightly lighter polygon inset
    panel.add(
        Polygon(
            vertices=((38.0, 82.0), (500.0, 76.0), (500.0, 200.0), (38.0, 204.0)),
            fill_color="#242D42",
            stroke_color="",
            stroke_width=0.0,
        )
    )
    scene.add_node(panel)
    scene.add_animation(0.0, 1.2, panel, MoveX(-90.0, 0.0))

    # Cool accent bar (left edge) — arrives with panel, then drifts slightly
    accent_bar = Node(x=0.0, y=0.0)
    accent_bar.add(
        Line(
            x0=0.0, y0=108.0,
            x1=0.0, y1=612.0,
            stroke_color=C_ACCENT_COOL,
            stroke_width=4.5,
        )
    )
    scene.add_node(accent_bar)
    scene.add_animation(0.15, 1.4, accent_bar, MoveX(-52.0, 48.0))
    # Subtle secondary drift after landing (gives it life)
    scene.add_animation(2.8, DURATION, accent_bar, MoveX(48.0, 44.0))

    # Horizontal rule — slides in from left after panel lands
    rule = Node(x=0.0, y=336.0)
    rule.add(
        Line(
            x0=0.0, y0=0.0,
            x1=640.0, y1=0.0,
            stroke_color=C_PANEL_EDGE,
            stroke_width=1.0,
        )
    )
    scene.add_node(rule)
    scene.add_animation(1.2, 2.2, rule, MoveX(-180.0, 68.0))

    # Right glyph: hex + triple ring system, warm gold accent
    glyph = Node(x=1020.0, y=348.0)
    # Inner hexagon — warm gold
    glyph.add(
        Polygon(
            vertices=_hexagon(72.0, phase=math.pi / 6),
            fill_color="#1E2840",
            stroke_color=C_ACCENT_WARM,
            stroke_width=2.5,
        )
    )
    # Inner hex fill accent (smaller hex, creates depth)
    glyph.add(
        Polygon(
            vertices=_hexagon(40.0, phase=math.pi / 6),
            fill_color="#252F48",
            stroke_color="#A08040",
            stroke_width=1.2,
        )
    )
    # Ring 1: cool cyan, close
    _ring(glyph, 108.0, 72, color=C_ACCENT_COOL, width=1.8)
    # Ring 2: warm gold, mid — counter-rotated for visual interest
    _ring(glyph, 134.0, 60, color=C_ACCENT_WARM, width=1.2, phase=math.pi / 60)
    # Ring 3: muted outer halo
    _ring(glyph, 162.0, 96, color="#354460", width=1.0)
    scene.add_node(glyph)
    # Arrives diagonally — sweeps in from bottom-right
    scene.add_animation(0.6, 2.4, glyph, Parallel(MoveX(1260.0, 1020.0), MoveY(500.0, 348.0)))
    # Slow breathing float after landing
    scene.add_animation(3.0, DURATION, glyph, MoveY(348.0, 338.0))

    # -----------------------------------------------------------------------
    # ACT 2 (t = 1.6 – 5.0): Text cascades in, left to right, top to bottom
    # -----------------------------------------------------------------------

    # Title — biggest, arrives first
    title = Text(
        content="ManimLite",
        x=80.0,
        y=104.0,
        font_size=58.0,
        color=C_TITLE,
    )
    scene.add_node(title)
    scene.add_animation(1.6, 2.8, title, MoveX(-560.0, 80.0))

    # Subtitle — 0.3 s after title
    subtitle = Text(
        content="Skia  ·  Typst  ·  PyAV",
        x=80.0,
        y=174.0,
        font_size=21.0,
        color=C_MUTED,
    )
    scene.add_node(subtitle)
    scene.add_animation(1.9, 3.1, subtitle, MoveX(-440.0, 80.0))

    # Tagline — 0.35 s after subtitle
    tag = Text(
        content="Motion without TeX Live. One pipeline, one cache, no frame files.",
        x=80.0,
        y=210.0,
        font_size=16.0,
        color=C_TAGLINE,
    )
    scene.add_node(tag)
    scene.add_animation(2.25, 3.5, tag, MoveX(-380.0, 80.0))

    # Formula — slides in from left with a slight upward component
    formula = MathExpr(
        typst_source="sum_(n=1)^infinity 1/n^2 = pi^2 / 6",
        x=92.0,
        y=262.0,
        font_size=34.0,
        color=C_TITLE,
    )
    scene.add_node(formula)
    scene.add_animation(2.7, 3.9, formula, Parallel(MoveX(-60.0, 92.0), MoveY(280.0, 262.0)))

    # Code block — rises from below the rule
    snippet = CodeBlock(
        code=(
            'from manimlite import Scene, MoveX, Text\n\n'
            "scene = Scene(width=1280, height=720, fps=30, duration=3.0)\n"
            "label = Text('Hello', x=80, y=120, font_size=42)\n"
            "scene.add_node(label)\n"
            "scene.add_animation(0.0, 2.0, label, MoveX(40.0, 120.0))\n"
        ),
        language="python",
        x=100.0,
        y=378.0,
        font_size=14.5,
    )
    scene.add_node(snippet)
    scene.add_animation(3.2, 4.6, snippet, MoveY(560.0, 378.0))

    # -----------------------------------------------------------------------
    # ACT 3 (t = 4.5 – end): Scene breathes — footer arrives last
    # -----------------------------------------------------------------------

    footer = Text(
        content="Render:  manimlite render examples/showcase_intro.py",
        x=80.0,
        y=666.0,
        font_size=14.0,
        color=C_MUTED,
    )
    scene.add_node(footer)
    # Footer sweeps in from the right — final punctuation
    scene.add_animation(4.5, 5.6, footer, MoveX(1340.0, 80.0))

    return scene


# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------

def get_skia_renderer() -> SkiaRenderer:
    """Optional hook for ``manimlite render`` — matches :func:`main` clear color."""
    return SkiaRenderer(clear_color=BG)


def main() -> None:
    scene = build_scene()
    out = Path("showcase_intro.mp4")
    renderer = SkiaRenderer(clear_color=BG)
    encoder = PyAVEncoder(scene=scene, output_path=out, renderer=renderer)
    result = encoder.encode(verbose=True)
    print(f"Output: {result} ({result.stat().st_size:,} bytes)", file=sys.stderr)


if __name__ == "__main__":
    main()