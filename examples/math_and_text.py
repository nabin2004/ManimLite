"""Showcase: Text + MathExpr (Typst) + CodeBlock + Circle animated and exported to MP4.

Run::

    python examples/math_and_text.py                     # renders to math_and_text.mp4
    manimlite render examples/math_and_text.py           # same, via CLI

Requires: skia-python, typst CLI on PATH.
"""

from __future__ import annotations

import sys
from pathlib import Path

from manimlite import (
    Circle,
    CircleOutline,
    MoveX,
    Scene,
    SkiaRenderer,
)
from manimlite.export import PyAVEncoder
from manimlite.text import CodeBlock, MathExpr, Text

WIDTH, HEIGHT = 1280, 720
FPS = 30.0
DURATION = 4.0


def build_scene() -> Scene:
    """Build a scene with text, math, code, and a circle — all animated."""
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)

    title = Text(
        content="ManimLite MVP",
        x=80,
        y=40,
        font_size=48.0,
        color="#61AFEF",
    )
    scene.add_node(title)
    scene.add_animation(0.0, 1.5, title, MoveX(80.0, 80.0))

    math = MathExpr(
        typst_source="sum_(k=1)^n k^2 = (n(n+1)(2n+1)) / 6",
        x=80,
        y=140,
        font_size=36.0,
        color="#FFFFFF",
    )
    scene.add_node(math)
    scene.add_animation(0.5, 2.5, math, MoveX(80.0, 80.0))

    code = CodeBlock(
        code="def fib(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a",
        language="python",
        x=80,
        y=280,
        font_size=16.0,
    )
    scene.add_node(code)

    circle = Circle(x=900, y=400, r=120, progress=0.0, fill_color="#E06C75")
    scene.add_node(circle)
    scene.add_animation(0.0, DURATION, circle, CircleOutline())
    scene.add_animation(1.0, DURATION, circle, MoveX(900.0, 700.0))

    subtitle = Text(
        content="Skia rendering + Typst math + PyAV encoding",
        x=80,
        y=620,
        font_size=20.0,
        color="#98C379",
    )
    scene.add_node(subtitle)

    return scene


def main() -> None:
    scene = build_scene()
    out = Path("math_and_text.mp4")
    encoder = PyAVEncoder(scene=scene, output_path=out)
    result = encoder.encode(verbose=True)
    print(f"Output: {result} ({result.stat().st_size:,} bytes)", file=sys.stderr)


if __name__ == "__main__":
    main()
