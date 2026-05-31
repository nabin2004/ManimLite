from motiongram.animate import Animation, MoveX
from motiongram.core import Node, Scene


def test_scene_and_timeline():
    scene = Scene()
    circle = Node()
    square = Node()
    scene.add_node(circle)
    scene.add_node(square)
    assert scene.root.children == [circle, square]

    scene.add_animation(0, 1, circle, MoveX(0.0, 10.0))
    scene.add_animation(1, 2, square, MoveX(0.0, 5.0))
    scene.add_animation(0.0, 1.0, circle, Animation().as_animator())

    assert len(scene.timeline.entries) == 3
    assert scene.timeline.entries[0][:2] == (0.0, 1.0)
    assert scene.timeline.entries[0][2] is circle