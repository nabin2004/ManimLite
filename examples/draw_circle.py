"""Draw circles on the terminal grid using the scene graph (single frame)."""

from __future__ import annotations

from motiongram import Circle, Renderer, Scene

WIDTH, HEIGHT = 32, 16
BG = " "


def main() -> None:
    r = Renderer(width=WIDTH, height=HEIGHT, bg=BG)
    scene = Scene(width=WIDTH, height=HEIGHT)
    scene.add_node(Circle(x=10, y=8, r=4, ch="N"))
    scene.add_node(Circle(x=20, y=8, r=4, ch="O"))
    r.render(scene)


if __name__ == "__main__":
    main()
