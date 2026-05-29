"""Showcase: Text, MathExpr (Typst), and CodeBlock capabilities in ManimLite.

This example demonstrates:
- Plain text rendering with various font sizes
- Mathematical expressions via Typst integration
- Syntax-highlighted code blocks with Pygments
- Animated text movements with a beautiful layout

Run::

    python examples/check_text.py                # renders to check_text.mp4
    manimlite render examples/check_text.py     # same, via CLI

Requires: skia-python, typst CLI on PATH, pygments, pyav
"""

from __future__ import annotations

import sys
from pathlib import Path

from manimlite import (
    Circle,
    CircleOutline,
    MoveX,
    MoveY,
    Scene,
    SkiaRenderer,
)
from manimlite.export import PyAVEncoder
from manimlite.text import CodeBlock, MathExpr, Text

WIDTH, HEIGHT = 1920, 1080
FPS = 30.0
DURATION = 8.0


def build_scene() -> Scene:
    """Build a scene showcasing text, math, and code rendering."""
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)

    # ─────────────────────────────────────────────────────────────
    # Title Section
    # ─────────────────────────────────────────────────────────────
    title = Text(
        content="ManimLite: Elegant Math Animations",
        x=100,
        y=80,
        font_size=64.0,
        color="#61AFEF",
    )
    scene.add_node(title)

    subtitle = Text(
        content="Flat design. Explicit timelines. Typst integration.",
        x=100,
        y=160,
        font_size=28.0,
        color="#98C379",
    )
    scene.add_node(subtitle)

    # ─────────────────────────────────────────────────────────────
    # Mathematical Expressions Section
    # ─────────────────────────────────────────────────────────────
    math_label = Text(
        content="Mathematical Expressions:",
        x=100,
        y=260,
        font_size=32.0,
        color="#C678DD",
    )
    scene.add_node(math_label)

    # Quadratic formula
    quadratic = MathExpr(
        typst_source="x = frac(-b plus.minus sqrt(b^2 - 4a c))(2a)",
        x=100,
        y=330,
        font_size=36.0,
        color="#6CDCE0",
    )
    scene.add_node(quadratic)
    scene.add_animation(0.5, 2.0, quadratic, MoveX(100.0, 100.0))

    # Summation
    summation = MathExpr(
        typst_source="S_n = sum_(k=1)^n k = frac(n(n+1))(2)",
        x=100,
        y=420,
        font_size=34.0,
        color="#56B6C2",
    )
    scene.add_node(summation)
    scene.add_animation(1.0, 2.5, summation, MoveX(100.0, 100.0))

    # Euler's formula
    euler = MathExpr(
        typst_source="e^(i pi) + 1 = 0",
        x=100,
        y=510,
        font_size=40.0,
        color="#E5C07B",
    )
    scene.add_node(euler)
    scene.add_animation(1.5, 3.0, euler, MoveX(100.0, 100.0))

    # ─────────────────────────────────────────────────────────────
    # Code Section
    # ─────────────────────────────────────────────────────────────
    code_label = Text(
        content="Syntax-Highlighted Code:",
        x=100,
        y=620,
        font_size=32.0,
        color="#C678DD",
    )
    scene.add_node(code_label)

    fibonacci_code = CodeBlock(
        code="def fib(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a+b\n    return a",
        language="python",
        x=100,
        y=700,
        font_size=18.0,
    )
    scene.add_node(fibonacci_code)
    scene.add_animation(2.5, 4.5, fibonacci_code, MoveX(100.0, 100.0))

    # ─────────────────────────────────────────────────────────────
    # Animation Features Section
    # ─────────────────────────────────────────────────────────────
    features_label = Text(
        content="Animation Features:",
        x=1050,
        y=260,
        font_size=32.0,
        color="#C678DD",
    )
    scene.add_node(features_label)

    feature1 = Text(
        content="✓ Flat composition over inheritance",
        x=1050,
        y=330,
        font_size=22.0,
        color="#FFFFFF",
    )
    scene.add_node(feature1)
    scene.add_animation(3.0, 4.5, feature1, MoveY(330.0, 330.0))

    feature2 = Text(
        content="✓ Explicit timeline-driven rendering",
        x=1050,
        y=380,
        font_size=22.0,
        color="#FFFFFF",
    )
    scene.add_node(feature2)
    scene.add_animation(3.5, 5.0, feature2, MoveY(380.0, 380.0))

    feature3 = Text(
        content="✓ Typst for beautiful math",
        x=1050,
        y=430,
        font_size=22.0,
        color="#FFFFFF" ,
    )
    scene.add_node(feature3)
    scene.add_animation(4.0, 5.5, feature3, MoveY(430.0, 430.0))

    feature4 = Text(
        content="✓ Pygments syntax highlighting",
        x=1050,
        y=480,
        font_size=22.0,
        color="#FFFFFF",
    )
    scene.add_node(feature4)
    scene.add_animation(4.5, 6.0, feature4, MoveY(480.0, 480.0))

    feature5 = Text(
        content="✓ PyAV video encoding",
        x=1050,
        y=530,
        font_size=22.0,
        color="#FFFFFF",
    )
    scene.add_node(feature5)
    scene.add_animation(5.0, 6.5, feature5, MoveY(530.0, 530.0))

    # ─────────────────────────────────────────────────────────────
    # Animated Circle
    # ─────────────────────────────────────────────────────────────
    circle = Circle(
        x=1400,
        y=650,
        r=180,
        progress=0.0,
        fill_color="#E06C75",
    )
    scene.add_node(circle)
    scene.add_animation(0.0, DURATION, circle, CircleOutline())
    scene.add_animation(2.0, DURATION, circle, MoveX(1400.0, 1200.0))

    # ─────────────────────────────────────────────────────────────
    # Closing Text
    # ─────────────────────────────────────────────────────────────
    closing = Text(
        content="Design for clarity. Code for control.",
        x=100,
        y=1000,
        font_size=24.0,
        color="#ABB2BF",
    )
    scene.add_node(closing)
    scene.add_animation(6.0, DURATION, closing, MoveY(1000.0, 1000.0))

    return scene


def main() -> None:
    scene = build_scene()
    out = Path("check_text.mp4")
    encoder = PyAVEncoder(scene=scene, output_path=out)
    result = encoder.encode(verbose=True)
    print(f"✓ Output: {result} ({result.stat().st_size:,} bytes)", file=sys.stderr)


if __name__ == "__main__":
    main()
