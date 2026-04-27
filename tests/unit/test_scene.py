from manimlite.core import Scene, Node

def test_scene_and_timeline():
    # Create a scene
    scene = Scene()

    # Create nodes
    circle = Node()
    square = Node()

    # Add nodes to the scene
    scene.add_node(circle)
    scene.add_node(square)

    # Assert that the nodes were added to the root's children
    assert scene.root.children == [circle, square]

    # Add animations to the timeline
    scene.add_animation(0, 1, circle, "animate_circle")
    scene.add_animation(1, 2, square, "animate_square")
    scene.add_animation(0.0, 1.0, circle, "fade_in")

    # # Assert that the animations were added to the timeline
    # assert scene.timeline.entries == (
    #     ((0.0, 1.0, Node(children=()), 'fade_in'),),
    #     (0, 1, circle, "animate_circle"),
    #     (1, 2, square, "animate_square"),
    # )