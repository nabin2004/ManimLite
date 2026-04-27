from dataclasses import dataclass, field

import pytest

from manimlite.animate import CircleOutline, MoveX, apply_timeline
from manimlite.core import Circle, Node, Scene
from manimlite.renderer import AsciiFrameCanvas, Renderer


@dataclass(slots=True)
class CountingNode(Node):
    hits: list[int] = field(default_factory=lambda: [0])

    def update(self, t: float, dt: float) -> None:
        self.hits[0] += 1
        Node.update(self, t, dt)


def test_set_pixel_in_bounds() -> None:
    r = Renderer(width=8, height=4, bg=" ")
    frame = r.blank_frame()
    r.set_pixel(frame, 2, 1)
    assert frame[1][2] == "#"
    assert frame[0][0] == " "


def test_set_pixel_out_of_bounds_noop() -> None:
    r = Renderer(width=8, height=4, bg=".")
    frame = r.blank_frame()
    for x, y in [(-1, 0), (8, 0), (0, -1), (0, 4), (100, 100)]:
        r.set_pixel(frame, x, y, "#")
    assert all(cell == "." for row in frame for cell in row)


def test_set_pixel_uses_first_character() -> None:
    r = Renderer(width=4, height=2, bg=" ")
    frame = r.blank_frame()
    r.set_pixel(frame, 0, 0, "@!")
    assert frame[0][0] == "@"


def test_set_pixel_empty_ch_noop() -> None:
    r = Renderer(width=4, height=2, bg=" ")
    frame = r.blank_frame()
    r.set_pixel(frame, 1, 1, "")
    assert frame[1][1] == " "


def test_render_scene_draws_circle_node(capsys) -> None:
    r = Renderer(width=32, height=16, bg=" ")
    scene = Scene(width=32, height=16)
    scene.add_node(Circle(x=10, y=8, r=3, ch="N"))
    r.render(scene)
    out = capsys.readouterr().out
    assert "N" in out


def test_render_propagates_parent_position(capsys) -> None:
    r = Renderer(width=40, height=14, bg=" ")
    scene = Scene(width=40, height=14)
    group = Node(x=6, y=2)
    group.add(Circle(x=8, y=6, r=2, ch="@"))
    scene.add_node(group)
    r.render(scene)
    assert "@" in capsys.readouterr().out


def test_node_update_visits_self_and_children() -> None:
    root = CountingNode()
    a = CountingNode()
    b = CountingNode()
    root.add(a)
    root.add(b)
    root.update(0.0, 1 / 30)
    assert root.hits[0] == 1
    assert a.hits[0] == 1
    assert b.hits[0] == 1


def test_play_calls_update_once_per_frame(capsys) -> None:
    r = Renderer(width=8, height=4, bg=" ")
    scene = Scene(width=8, height=4, fps=10.0, duration=0.2)
    counter = CountingNode()
    scene.add_node(counter)
    r.play(scene, realtime=False)
    _ = capsys.readouterr()
    assert counter.hits[0] == 2


def test_circle_progress_partial_draw() -> None:
    r = Renderer(width=32, height=16, bg=" ")
    scene = Scene(width=32, height=16)
    c = Circle(x=10, y=8, r=3, ch="N", progress=1.0)
    scene.add_animation(0.0, 1.0, c, CircleOutline())
    apply_timeline(scene, 0.0, ease=None)
    frame = r.blank_frame()
    canvas = AsciiFrameCanvas(r, frame)
    c.draw(canvas, 0.0, 0.0)
    assert "N" not in "".join("".join(row) for row in frame)
    apply_timeline(scene, 1.0, ease=None)
    frame = r.blank_frame()
    canvas = AsciiFrameCanvas(r, frame)
    c.draw(canvas, 0.0, 0.0)
    assert "N" in "".join("".join(row) for row in frame)


def test_play_advances_circle_progress(capsys) -> None:
    r = Renderer(width=32, height=16, bg=" ")
    scene = Scene(width=32, height=16, fps=10.0, duration=1.0)
    c = Circle(x=10, y=8, r=3, ch="N", progress=0.0)
    scene.add_node(c)
    scene.add_animation(0.0, 1.0, c, CircleOutline())
    r.play(scene, realtime=False)
    _ = capsys.readouterr()
    assert c.progress >= 1.0 - 1e-9


def test_render_applies_timeline_at_zero(capsys) -> None:
    r = Renderer(width=32, height=16, bg=" ")
    scene = Scene(width=32, height=16)
    n = Node(x=0.0)
    scene.add_node(n)
    scene.add_animation(0.0, 1.0, n, MoveX(10.0, 20.0))
    r.render(scene)
    _ = capsys.readouterr()
    assert n.x == 10.0


def test_play_logs_timeline_to_stderr_when_debug(capsys) -> None:
    r = Renderer(width=8, height=4, bg=" ", debug=True)
    scene = Scene(width=8, height=4, fps=10.0, duration=0.1)
    n = Node()
    scene.add_node(n)
    scene.add_animation(0.0, 1.0, n, MoveX(0.0, 1.0))
    r.play(scene, realtime=False)
    err = capsys.readouterr().err
    assert "[t=" in err
    assert "MoveX" in err


def test_play_move_x_reaches_end(capsys) -> None:
    r = Renderer(width=8, height=4, bg=" ")
    scene = Scene(width=8, height=4, fps=10.0, duration=1.0)
    n = Node()
    scene.add_node(n)
    scene.add_animation(0.0, 1.0, n, MoveX(0.0, 100.0))
    r.play(scene, realtime=False)
    _ = capsys.readouterr()
    assert n.x == 100.0


def test_play_rejects_non_positive_fps() -> None:
    r = Renderer(width=8, height=4, bg=" ")
    scene = Scene(width=8, height=4, fps=0.0, duration=1.0)
    with pytest.raises(ValueError, match="fps"):
        r.play(scene)
