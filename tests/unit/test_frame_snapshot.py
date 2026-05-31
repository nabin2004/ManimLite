"""Deterministic ASCII frame snapshots."""

from __future__ import annotations

from motiongram.animate import CircleOutline
from motiongram.core import Circle, Scene
from motiongram.engine import step_frame
from motiongram.renderer import AsciiFrameCanvas, Renderer, ascii_frame_sha256


def _render_still_at_t(scene: Scene, t: float, r: Renderer) -> list[list[str]]:
    step_frame(scene, t, 1.0 / scene.fps, ease=None)
    frame = r.blank_frame()
    scene.root.draw(AsciiFrameCanvas(r, frame), 0.0, 0.0)
    return frame


def test_same_scene_two_passes_identical_frame_digest() -> None:
    """Frame content at a fixed time must be bitwise reproducible."""

    def build() -> tuple[Scene, Renderer]:
        scene = Scene(width=24, height=12, fps=30.0, duration=1.0)
        r = Renderer(width=24, height=12, bg=" ")
        circ = Circle(x=11, y=5, r=3, ch="@", progress=0.0)
        scene.add_node(circ)
        scene.add_animation(0.0, 1.0, circ, CircleOutline())
        return scene, r

    s1, r1 = build()
    s2, r2 = build()
    f1 = _render_still_at_t(s1, 0.73, r1)
    f2 = _render_still_at_t(s2, 0.73, r2)

    d1 = ascii_frame_sha256(f1)
    d2 = ascii_frame_sha256(f2)
    assert d1 == d2
    assert len(d1) == 64
