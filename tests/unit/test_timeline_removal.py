"""Timeline removal: disabling one animator must not corrupt others."""

from __future__ import annotations

import pytest

from manimlite.animate import CircleOutline, MoveX, apply_timeline
from manimlite.core import Circle, Node, Scene, Timeline


def test_remove_animation_at_leaves_other_entry_intact() -> None:
    a = Node(x=0.0)
    b = Circle(x=1.0, y=1.0, r=2.0, progress=0.0)
    scene = Scene()
    scene.add_node(a)
    scene.add_node(b)
    scene.add_animation(0.0, 1.0, a, MoveX(0.0, 100.0))
    scene.add_animation(0.0, 1.0, b, CircleOutline())

    scene.remove_animation_at(0)

    apply_timeline(scene, 0.5, ease=None)

    assert a.x == 0.0  # MoveX gone — still initial
    assert b.progress == 0.5


def test_without_entry_raises_on_bad_index() -> None:
    t = Timeline().add(0.0, 1.0, Node(), MoveX(0.0, 1.0))
    with pytest.raises(IndexError):
        t.without_entry(-1)
    with pytest.raises(IndexError):
        t.without_entry(42)
