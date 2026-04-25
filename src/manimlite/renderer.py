from manimlite.core import Scene

class Renderer:
    def __init__(self, width: int = 1920, height: int = 1080, fps: float = 30.0, bg: str = "black"):
        self.width = width
        self.height = height
        self.fps = fps
        self.bg = bg
        self.scene = Scene(width=width, height=height, fps=fps)

    def blank_frame(self) -> None:
        """Create a blank frame with the bacckground character."""
        return [[self.bg for _ in range(self.width)] for _ in range(self.height)]
    
    def render(self, scene: Scene) -> None:
        """Render the scene to the terminal"""
        frame = self.blank_frame()
        self._draw_node(scene.root, frame)
        self.show(frame)

    def _draw_node(self, node, frame: list[list[str]]) -> None:
        """Recursively draw a node and its children onto the frame."""
        node.draw(frame)
        for child in node.children:
            self._draw_node(child, frame)

    def show(self, frame: list[list[str]]) -> None:
        """Print the frame to the terminal."""
        for row in frame:
            print("".join(row))
