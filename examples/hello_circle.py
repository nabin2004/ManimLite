"""Example scene: animated circle (TODO — implement render pipeline)."""

from __future__ import annotations

from typmotion import Scene
from typmotion.shapes import Circle


def build_scene() -> Scene:
    """Return a minimal scene with a circle (graph wiring TBD)."""
    scene = Scene(width=1280, height=720, fps=30, duration=2.0)
    _ = Circle(radius=80.0, fill_color="#4FC3F7")
    # TODO: attach circle to scene.root and add timeline animations.
    return scene


if __name__ == "__main__":
    _ = build_scene()
