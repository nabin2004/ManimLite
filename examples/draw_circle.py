"""Draw circles on the terminal grid using the scene graph and a simple play loop."""

from __future__ import annotations

from dataclasses import dataclass

from manimlite import Circle, Node, Renderer, Scene

WIDTH, HEIGHT = 32, 16
BG = " "
FPS = 10.0
DURATION = 2.0


@dataclass(slots=True)
class DriftingCircle(Circle):
    """Example-only motion; library Circle stays static unless you subclass update()."""

    def update(self, t: float, dt: float) -> None:
        self.x += 5.0 * dt
        Node.update(self, t, dt)


def main() -> None:
    r = Renderer(width=WIDTH, height=HEIGHT, fps=FPS, bg=BG)
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    scene.add_node(Circle(x=10, y=8, r=4, ch="N"))
    scene.add_node(DriftingCircle(x=20, y=8, r=4, ch="O"))
    r.play(scene)


if __name__ == "__main__":
    main()
