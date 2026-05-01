"""Same scene as ``play_circles.py``, with an optional ASCII still snapshot.

Time-stepped: ``CircleOutline`` reveals outlines; ``MoveX`` slides the right circle. Setup uses
``progress=0.0`` so timeline-driven motion owns the clip (see ``play_circles.py`` docstring).

Run::

    python showcase_play_circles.py          # print end-frame ASCII + numeric state

To watch frames in the terminal (realtime pacing)::

    python play_circles.py
    python examples/showcase_play_circles.py --play 
"""

from __future__ import annotations

import os
import sys

from manimlite import Circle, CircleOutline, MoveX, Renderer, Scene, step_frame
from manimlite.renderer import AsciiFrameCanvas, ascii_frame_text

WIDTH, HEIGHT = 32, 16
BG = " "
FPS = 10.0
DURATION = 2.0


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    left = Circle(x=10, y=8, r=4, ch="N", progress=0.0)
    right = Circle(x=20, y=8, r=4, ch="O", progress=0.0)
    scene.add_node(left)
    scene.add_node(right)
    scene.add_animation(0.0, DURATION, left, CircleOutline())
    scene.add_animation(0.0, DURATION, right, CircleOutline())
    scene.add_animation(0.0, DURATION, right, MoveX(20.0, 20.0 + 5.0 * DURATION))
    return scene


def ascii_still(scene: Scene, t: float, r: Renderer) -> str:
    dt = 1.0 / scene.fps
    step_frame(scene, t, dt)
    frame = r.blank_frame()
    scene.root.draw(AsciiFrameCanvas(r, frame), 0.0, 0.0)
    return ascii_frame_text(frame)


def main() -> None:
    if "--play" in sys.argv or os.environ.get("RUN_PLAYBACK") == "1":
        r = Renderer(width=WIDTH, height=HEIGHT, fps=FPS, bg=BG)
        r.play(build_scene())
        return

    scene = build_scene()
    r = Renderer(width=WIDTH, height=HEIGHT, fps=FPS, bg=BG)
    dt = 1.0 / scene.fps

    print("Showcase: play_circles scene (headless snapshots)\n")

    # t=0: timeline at start (left endpoint of segments)
    step_frame(scene, 0.0, dt)
    frame0 = r.blank_frame()
    scene.root.draw(AsciiFrameCanvas(r, frame0), 0.0, 0.0)
    print("--- t = 0.0 (start of timeline segments) ---")
    print(ascii_frame_text(frame0))
    left, right = scene.root.children
    assert isinstance(left, Circle) and isinstance(right, Circle)
    print(f"left.progress={left.progress:.4f}  right.progress={right.progress:.4f}  right.x={right.x:.4f}\n")

    scene = build_scene()
    print(f"--- t = {DURATION} (end of clip, smoothstep easing) ---")
    print(ascii_still(scene, DURATION, r))
    left, right = scene.root.children
    print(f"left.progress={left.progress:.4f}  right.progress={right.progress:.4f}  right.x={right.x:.4f}\n")

    print("Terminal playback:  python examples/play_circles.py")
    print("Or:                 RUN_PLAYBACK=1 python examples/showcase_play_circles.py")
    print("Or:                 python examples/showcase_play_circles.py --play")


if __name__ == "__main__":
    main()
