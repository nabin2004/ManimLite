"""Showcase deep-learning explainer nodes: Matrices, HiddenLayers, ActivationFunctions, Convolutions.

Renders a short Skia MP4 when run directly::

    PYTHONPATH=src python examples/deeplearning_showcase.py

Use ``--dry-run`` to verify scene construction without encoding.
"""

from __future__ import annotations

import sys
from pathlib import Path

from motiongram import Scene
from motiongram.deeplearning import (
    ActivationFunctions,
    AnimateAttribute,
    AnimateIntAttribute,
    Convolutions,
    HiddenLayers,
    Matrices,
)
from motiongram.export import PyAVEncoder
from motiongram.render import SkiaRenderer

WIDTH = 1280
HEIGHT = 720
FPS = 30.0
DURATION = 8.0
BG = (33, 37, 43)  # #21252b


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)

    weights = Matrices(
        x=80,
        y=100,
        values=[
            [0.2, -0.5, 0.1, 0.0],
            [0.8, 0.3, -0.2, 0.6],
            [0.0, 0.6, 0.4, -0.1],
        ],
        label="Weight matrix W",
        highlight_row=0,
    )
    scene.add_node(weights)
    scene.add_animation(0.0, 4.0, weights, AnimateIntAttribute("highlight_row", 0, 2))

    net = HiddenLayers(
        x=520,
        y=80,
        layer_sizes=[3, 5, 5, 2],
        progress=0.0,
    )
    scene.add_node(net)
    scene.add_animation(0.0, DURATION, net, AnimateAttribute("progress", 0.0, 1.0))

    relu = ActivationFunctions(
        x=80,
        y=380,
        activation="relu",
        input_val=-2.5,
        width=320,
        height=200,
    )
    scene.add_node(relu)
    scene.add_animation(0.0, 5.0, relu, AnimateAttribute("input_val", -2.5, 3.0))

    conv = Convolutions(
        x=520,
        y=380,
        input_grid=[
            [1.0, 0.0, 1.0, 0.0],
            [0.0, 1.0, 0.0, 1.0],
            [1.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 1.0],
        ],
        kernel=[[1.0, 0.0], [0.0, 1.0]],
        kernel_row=0,
        kernel_col=0,
    )
    scene.add_node(conv)
    scene.add_animation(0.0, 6.0, conv, AnimateIntAttribute("kernel_col", 0, 2))
    scene.add_animation(2.0, 6.0, conv, AnimateIntAttribute("kernel_row", 0, 2))

    return scene


def main() -> None:
    scene = build_scene()
    if "--dry-run" in sys.argv:
        print("Scene OK:", len(scene.timeline.entries), "animations")
        return

    out = Path("deeplearning_showcase.mp4")
    encoder = PyAVEncoder(
        scene=scene,
        output_path=out,
        renderer=SkiaRenderer(clear_color=BG),
    )
    result = encoder.encode(verbose=True)
    print(f"Wrote: {result}", file=sys.stderr)


if __name__ == "__main__":
    main()
