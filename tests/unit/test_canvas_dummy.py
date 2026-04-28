"""Dummy vs ASCII backends: timeline state must not depend on canvas implementation."""

from __future__ import annotations

from manimlite.animate import CircleOutline, MoveX
from manimlite.canvas import NullCanvas, RecordingCanvas
from manimlite.core import Circle, Node, Scene
from manimlite.engine import step_frame
from manimlite.renderer import AsciiFrameCanvas, Renderer


def _paired_scenes():
    """Two logically identical scenes (separate graphs for isolation)."""

    def one():
        s = Scene(width=16, height=8, fps=30.0, duration=1.0)
        n = Node(x=0.0)
        c = Circle(x=2.0, y=2.0, r=2.0, ch="X", progress=0.0)
        s.add_node(n)
        s.add_node(c)
        s.add_animation(0.0, 1.0, n, MoveX(0.0, 10.0))
        s.add_animation(0.0, 1.0, c, CircleOutline())
        return s, n, c

    return one(), one()


def test_step_frame_same_state_for_two_scenes() -> None:
    (s1, n1, c1), (s2, n2, c2) = _paired_scenes()
    dt = 1.0 / 30.0
    t = 0.4
    step_frame(s1, t, dt, ease=None)
    step_frame(s2, t, dt, ease=None)
    assert n1.x == n2.x == 4.0
    assert c1.progress == c2.progress == 0.4


def test_draw_does_not_mutate_timeline_driven_state() -> None:
    (s1, n1, c1), _ = _paired_scenes()
    dt = 1.0 / 30.0
    step_frame(s1, 0.5, dt, ease=None)
    x_before, p_before = n1.x, c1.progress

    n1.draw(NullCanvas(), 0.0, 0.0)
    c1.draw(NullCanvas(), 0.0, 0.0)
    assert n1.x == x_before and c1.progress == p_before

    rec = RecordingCanvas()
    c1.draw(rec, 0.0, 0.0)
    assert c1.progress == p_before
    assert len(rec.ops) > 0


def test_dummy_vs_ascii_same_node_state_after_step() -> None:
    (s_null, n_a, c_a), (s_ascii, n_b, c_b) = _paired_scenes()
    r = Renderer(width=16, height=8, bg=" ")
    dt = 1.0 / 30.0
    t = 0.35
    step_frame(s_null, t, dt, ease=None)
    step_frame(s_ascii, t, dt, ease=None)

    n_a.draw(NullCanvas())
    frame = r.blank_frame()
    n_b.draw(AsciiFrameCanvas(r, frame))
    c_a.draw(NullCanvas())
    c_b.draw(AsciiFrameCanvas(r, r.blank_frame()))

    assert n_a.x == n_b.x
    assert c_a.progress == c_b.progress
