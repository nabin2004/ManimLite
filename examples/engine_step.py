"""Advance scene time with ``step_frame`` only (no ``Renderer.play`` / terminal frames).

Use this pattern for headless tests, Skia frame export, or debug: animation state comes from the
timeline + ``apply_timeline``; ``step_frame`` also runs ``Node.update`` for non-spatial hooks.
"""

from __future__ import annotations

from typmotion import Circle, CircleOutline, Scene, step_frame


def main() -> None:
    scene = Scene(width=48, height=24, fps=30.0, duration=1.0)
    c = Circle(x=20, y=12, r=6, ch="*", progress=0.0)
    scene.add_node(c)
    scene.add_animation(0.0, 1.0, c, CircleOutline())

    dt = 1.0 / scene.fps
    for t in (0.0, 0.25, 0.5, 1.0):
        step_frame(scene, t, dt, ease=None)
        print(f"t={t:4.2f}  progress={c.progress:.4f}")


if __name__ == "__main__":
    main()
