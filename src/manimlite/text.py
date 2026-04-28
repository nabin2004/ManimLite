"""Text, math (Typst), and syntax-highlighted code blocks (implementation pending)."""

from __future__ import annotations

from dataclasses import dataclass

from manimlite.canvas import Canvas
from manimlite.core import Node


@dataclass(slots=True)
class Text(Node):
    """Plain text label."""

    content: str = ""
    font_size: float = 24.0
    color: str = "#FFFFFF"

    def draw(self, canvas: Canvas, ox: float = 0.0, oy: float = 0.0) -> None:
        """Rasterize text via Skia (stub)."""
        _ = canvas, ox, oy
        Node.draw(self, canvas, ox, oy)


@dataclass(slots=True)
class MathExpr(Node):
    """Mathematical expression rendered via Typst to cached SVG."""

    typst_source: str = ""
    font_size: float = 28.0
    color: str = "#FFFFFF"

    def draw(self, canvas: Canvas, ox: float = 0.0, oy: float = 0.0) -> None:
        """Typst → cached SVG; Skia canvases implement ``draw_svg_bytes``."""
        px = ox + self.x
        py = oy + self.y
        if self.typst_source.strip():
            from manimlite.typst_cache import cached_typst_svg_path

            svg_path = cached_typst_svg_path(self.typst_source)
            if svg_path is not None:
                data = svg_path.read_bytes()
                place = getattr(canvas, "draw_svg_bytes", None)
                if place is not None:
                    scale = max(self.font_size, 1.0) / 28.0
                    place(data, px, py, scale)
        Node.draw(self, canvas, ox, oy)


@dataclass(slots=True)
class CodeBlock(Node):
    """Source code with Pygments highlighting."""

    code: str = ""
    language: str = "python"
    font_size: float = 14.0

    def draw(self, canvas: Canvas, ox: float = 0.0, oy: float = 0.0) -> None:
        """Highlight and draw code (stub)."""
        _ = canvas, ox, oy
        Node.draw(self, canvas, ox, oy)
