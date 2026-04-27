"""Text, math (Typst), and syntax-highlighted code blocks (implementation pending)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from manimlite.core import Node


@dataclass(slots=True)
class Text(Node):
    """Plain text label."""

    content: str = ""
    font_size: float = 24.0
    color: str = "#FFFFFF"

    def draw(self, canvas: Any, ox: float = 0.0, oy: float = 0.0) -> None:
        """Rasterize text via Skia (stub)."""
        _ = canvas, ox, oy
        Node.draw(self, canvas, ox, oy)


@dataclass(slots=True)
class MathExpr(Node):
    """Mathematical expression rendered via Typst to cached SVG."""

    typst_source: str = ""
    font_size: float = 28.0
    color: str = "#FFFFFF"

    def draw(self, canvas: Any, ox: float = 0.0, oy: float = 0.0) -> None:
        """Render Typst → SVG → Skia (stub)."""
        _ = canvas, ox, oy
        Node.draw(self, canvas, ox, oy)


@dataclass(slots=True)
class CodeBlock(Node):
    """Source code with Pygments highlighting."""

    code: str = ""
    language: str = "python"
    font_size: float = 14.0

    def draw(self, canvas: Any, ox: float = 0.0, oy: float = 0.0) -> None:
        """Highlight and draw code (stub)."""
        _ = canvas, ox, oy
        Node.draw(self, canvas, ox, oy)
