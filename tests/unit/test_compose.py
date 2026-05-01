import pytest

from manimlite.animate import (
    CircleOutline,
    Delay,
    MoveX,
    MoveY,
    Parallel,
    Sequence,
    apply_timeline,
)
from manimlite.core import Circle, Node, Scene


def test_parallel_movex_and_circle_outline() -> None:
    scene = Scene(width=32, height=16)
    c = Circle(x=0.0, y=0.0, r=2.0, ch="N", progress=0.0)
    scene.add_node(c)
    scene.add_animation(0.0, 1.0, c, Parallel(MoveX(0.0, 10.0), CircleOutline()))
    apply_timeline(scene, 0.5, ease=None)
    assert c.x == 5.0
    assert c.progress == 0.5


def test_sequence_two_movex() -> None:
    scene = Scene()
    n = Node(x=0.0)
    scene.add_node(n)
    scene.add_animation(0.0, 1.0, n, Sequence(MoveX(0.0, 10.0), MoveX(10.0, 20.0)))
    apply_timeline(scene, 0.25, ease=None)
    assert n.x == 5.0
    apply_timeline(scene, 0.75, ease=None)
    assert n.x == 15.0


def test_delay_runs_inner_mid_window() -> None:
    scene = Scene()
    c = Circle(x=0.0, y=0.0, r=2.0, ch="N", progress=0.0)
    scene.add_node(c)
    scene.add_animation(0.0, 1.0, c, Delay(CircleOutline(), 0.25, 0.75))
    apply_timeline(scene, 0.5, ease=None)
    assert c.progress == 0.5
    c.progress = 0.0
    apply_timeline(scene, 0.1, ease=None)
    assert c.progress == 0.0


def test_delay_invalid_range_raises() -> None:
    with pytest.raises(ValueError, match="Delay"):
        Delay(CircleOutline(), 0.5, 0.5)


def test_parallel_movex_and_movey() -> None:
    n = Node(x=0.0, y=0.0)
    scene = Scene()
    scene.add_node(n)
    scene.add_animation(0.0, 1.0, n, Parallel(MoveX(0.0, 10.0), MoveY(0.0, 20.0)))
    apply_timeline(scene, 0.5, ease=None)
    assert n.x == 5.0
    assert n.y == 10.0
