"""Slide deck: MLP intro with Typst math, horizontal slide transitions, 15 s.

Uses ``MathExpr`` (Typst) for formulas and ``Text`` for titles. Each slide is a
parent ``Node``; transitions are ``Parallel(MoveX(...), FadeIn/FadeOut)``.

Run::

    python examples/mlp_slides_typst.py
    motiongram render examples/mlp_slides_typst.py -o mlp_slides.mp4

Requires: skia-python, ``typst`` on ``PATH``.
"""

from __future__ import annotations

import sys
from pathlib import Path

from motiongram import (
    FadeIn,
    FadeOut,
    MoveX,
    Node,
    Parallel,
    Scene,
    SkiaRenderer,
)
from motiongram.export import PyAVEncoder
from motiongram.text import MathExpr, Text

WIDTH, HEIGHT = 1280, 720
FPS = 30.0
DURATION = 15.0

BG = (18, 20, 28)
C_TITLE = "#61AFEF"
C_BODY = "#ABB2BF"
C_ACCENT = "#E5C07B"
C_MATH = "#FFFFFF"

# Off-screen right / home / exit left for slide roots
X_ENTER = float(WIDTH) + 180.0
X_HOME = 72.0
X_EXIT = -480.0
Y_SLIDE = 96.0

DT_IN = 0.48
DT_OUT = 0.48


def _add_slide_timeline(
    scene: Scene,
    *,
    root: Node,
    t0: float,
    span: float,
    with_exit: bool,
) -> None:
    """Enter ``[t0, t0+DT_IN]``, optional exit ``[t0+span-DT_OUT, t0+span]``."""
    t1 = t0 + DT_IN
    scene.add_animation(t0, t1, root, Parallel(MoveX(X_ENTER, X_HOME), FadeIn(0.0, 1.0)))
    if with_exit:
        scene.add_animation(
            t0 + span - DT_OUT,
            t0 + span,
            root,
            Parallel(MoveX(X_HOME, X_EXIT), FadeOut(1.0, 0.0)),
        )


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)

    unit = DURATION / 5.0

    # --- Slide 1: title -------------------------------------------------
    s1 = Node(x=X_ENTER, y=Y_SLIDE, opacity=0.0)
    s1.add(
        Text(
            content="Multi-layer perceptron",
            x=0,
            y=0,
            font_size=52.0,
            color=C_TITLE,
        )
    )
    s1.add(
        Text(
            content="Feedforward nets, one slide at a time · 15 s primer",
            x=0,
            y=72,
            font_size=22.0,
            color=C_BODY,
        )
    )
    scene.add_node(s1)
    _add_slide_timeline(scene, root=s1, t0=0.0, span=unit, with_exit=True)

    # --- Slide 2: idea --------------------------------------------------
    s2 = Node(x=X_ENTER, y=Y_SLIDE, opacity=0.0)
    s2.add(
        Text(
            content="What it is",
            x=0,
            y=0,
            font_size=40.0,
            color=C_TITLE,
        )
    )
    s2.add(
        Text(
            content="Stack affine transforms (weights W and biases b)",
            x=0,
            y=64,
            font_size=26.0,
            color=C_BODY,
        )
    )
    s2.add(
        Text(
            content="Between layers, apply a nonlinearity σ (ReLU, sigmoid, …)",
            x=0,
            y=110,
            font_size=26.0,
            color=C_BODY,
        )
    )
    s2.add(
        Text(
            content="Input → hidden → … → output (supervised learning fits W, b)",
            x=0,
            y=168,
            font_size=22.0,
            color=C_ACCENT,
        )
    )
    scene.add_node(s2)
    _add_slide_timeline(scene, root=s2, t0=unit, span=unit, with_exit=True)

    # --- Slide 3: one layer (Typst) ------------------------------------
    s3 = Node(x=X_ENTER, y=Y_SLIDE, opacity=0.0)
    s3.add(
        Text(
            content="One layer (vector form)",
            x=0,
            y=0,
            font_size=36.0,
            color=C_TITLE,
        )
    )
    s3.add(
        MathExpr(
            typst_source="bold(y) = sigma( bold(W) bold(x) + bold(b) )",
            x=0,
            y=76,
            font_size=32.0,
            color=C_MATH,
        )
    )
    s3.add(
        Text(
            content="σ acts element-wise; W and b match each layer's input/output width",
            x=0,
            y=168,
            font_size=20.0,
            color=C_BODY,
        )
    )
    scene.add_node(s3)
    _add_slide_timeline(scene, root=s3, t0=2 * unit, span=unit, with_exit=True)

    # --- Slide 4: depth (Typst) -----------------------------------------
    s4 = Node(x=X_ENTER, y=Y_SLIDE, opacity=0.0)
    s4.add(
        Text(
            content="Depth: layer ell",
            x=0,
            y=0,
            font_size=36.0,
            color=C_TITLE,
        )
    )
    s4.add(
        MathExpr(
            typst_source="bold(h)_ell = sigma( bold(W)_ell bold(h)_(ell - 1) + bold(b)_ell )",
            x=0,
            y=72,
            font_size=30.0,
            color=C_MATH,
        )
    )
    s4.add(
        Text(
            content="Without σ, many layers collapse to a single affine map",
            x=0,
            y=162,
            font_size=22.0,
            color=C_ACCENT,
        )
    )
    s4.add(
        MathExpr(
            typst_source="op(\"ReLU\")(z) = max(0, z)",
            x=0,
            y=210,
            font_size=26.0,
            color=C_BODY,
        )
    )
    scene.add_node(s4)
    _add_slide_timeline(scene, root=s4, t0=3 * unit, span=unit, with_exit=True)

    # --- Slide 5: recap (stays to end) ----------------------------------
    s5 = Node(x=X_ENTER, y=Y_SLIDE, opacity=0.0)
    s5.add(
        Text(
            content="Takeaway",
            x=0,
            y=0,
            font_size=40.0,
            color=C_TITLE,
        )
    )
    s5.add(
        Text(
            content="MLP = alternating linear maps + σ  →  expressive, trainable with backprop",
            x=0,
            y=70,
            font_size=24.0,
            color=C_BODY,
        )
    )
    s5.add(
        Text(
            content="Typst math above is rendered to SVG and composited like any other node",
            x=0,
            y=120,
            font_size=20.0,
            color=C_ACCENT,
        )
    )
    scene.add_node(s5)
    _add_slide_timeline(scene, root=s5, t0=4 * unit, span=unit, with_exit=False)

    return scene


def main() -> None:
    scene = build_scene()
    out = Path(__file__).with_suffix(".mp4")
    encoder = PyAVEncoder(
        scene=scene,
        output_path=out,
        renderer=SkiaRenderer(clear_color=BG),
    )
    result = encoder.encode(verbose=True)
    print(f"Output: {result} ({result.stat().st_size:,} bytes)", file=sys.stderr)


if __name__ == "__main__":
    main()