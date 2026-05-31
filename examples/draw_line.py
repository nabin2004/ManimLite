"""Draw a line on the terminal grid - Phase 006 style."""

from __future__ import annotations

from motiongram import Renderer

WIDTH, HEIGHT = 32, 16
BG = " "


def main() -> None:
    r = Renderer(width=WIDTH, height=HEIGHT, bg=BG)
    frame = r.blank_frame()
    r.line(frame, x1=0, y1=0, x2=30, y2=30, ch="\\")
    r.show(frame)


if __name__ == "__main__":
    main()
