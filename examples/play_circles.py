"""Time-stepped scene: timeline-driven outline reveal and horizontal move (interpolation)."""

from __future__ import annotations

from manimlite import Circle, CircleOutline, MoveX, Renderer, Scene

WIDTH, HEIGHT = 32, 16
BG = " "
FPS = 10.0
DURATION = 2.0


def main() -> None:
    r = Renderer(width=WIDTH, height=HEIGHT, fps=FPS, bg=BG)
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    left = Circle(x=10, y=8, r=4, ch="N", progress=0.0)
    right = Circle(x=20, y=8, r=4, ch="O", progress=0.0)
    scene.add_node(left)
    scene.add_node(right)
    scene.add_animation(0.0, DURATION, left, CircleOutline())
    scene.add_animation(0.0, DURATION, right, CircleOutline())
    # ~5 units/sec over DURATION matches prior drift feel (smoothstep via apply_timeline default)
    scene.add_animation(0.0, DURATION, right, MoveX(20.0, 20.0 + 5.0 * DURATION))
    r.play(scene)


if __name__ == "__main__":
    main()
