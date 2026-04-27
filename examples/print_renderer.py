"""Print a frame to the terminal — Phase 005 style (small grid, space background)."""

from __future__ import annotations

from manimlite import Renderer

WIDTH, HEIGHT = 32, 16
BG = " "


def main() -> None:
    r = Renderer(width=WIDTH, height=HEIGHT, bg=BG)
    frame = r.blank_frame()
    r.show(frame)


if __name__ == "__main__":
    main()
