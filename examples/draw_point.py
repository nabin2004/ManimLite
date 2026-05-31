"""Draw one pixel on the terminal grid — Phase 006 style."""

from __future__ import annotations

from motiongram import Renderer

WIDTH, HEIGHT = 32, 16
BG = " "


def main() -> None:
    r = Renderer(width=WIDTH, height=HEIGHT, bg=BG)
    frame = r.blank_frame()
    r.set_pixel(frame, 0, 0, ch="N")
    r.show(frame)


if __name__ == "__main__":
    main()
