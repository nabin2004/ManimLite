"""Draw a circle on the terminal grid - Phase 006 style."""

from __future__ import annotations

from manimlite import Renderer

WIDTH, HEIGHT = 32, 16
BG = " "


def main() -> None:
    r = Renderer(width=WIDTH, height=HEIGHT, bg=BG)
    frame = r.blank_frame()
    r.circle(frame, cx=10, cy=8, r=4, ch="N")
    r.circle(frame, cx=20, cy=8, r=4, ch="O")
    r.show(frame)


if __name__ == "__main__":
    main()
