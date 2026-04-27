from manimlite.core import Scene

class Renderer:
    def __init__(self, width: int = 1920, height: int = 1080, fps: float = 30.0, bg: str = "black"):
        self.width = width
        self.height = height
        self.fps = fps
        self.bg = bg
        self.scene = Scene(width=width, height=height, fps=fps)

    def blank_frame(self) -> list[list[str]]:
        """Create a blank frame with the background character."""
        return [[self.bg for _ in range(self.width)] for _ in range(self.height)]

    def set_pixel(self, frame: list[list[str]], x: int, y: int, ch: str = "#") -> None:
        """Write one character to the frame; out-of-bounds writes are clipped."""
        if not ch:
            return
        if not (0 <= x < self.width and 0 <= y < self.height):
            return
        frame[y][x] = ch[0]

    def line(self, frame: list[list[str]], x1: int, y1: int, x2: int, y2: int, ch: str = "#") -> None:
        """Draw a line from (x1, y1) to (x2, y2) using Bresenham's line algorithm."""
        pass 

    def circle(self, frame: list[list[str]], cx: int, cy: int, r: int, ch: str = "#") -> None:
        """Draw a circle centered at (cx, cy) with radius r using the midpoint circle algorithm."""
        pass

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
