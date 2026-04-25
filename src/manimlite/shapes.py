"""Vector primitives: circle, line, polygon (implementation pending)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from manimlite.core import Node


@dataclass(slots=True)
class Circle(Node):
    """Circle centered in local coordinates."""

    radius: float = 100.0
    fill_color: str = "#FFFFFF"
    stroke_color: str | None = None
    stroke_width: float = 0.0

    def draw(self, canvas: Any) -> None:
        """Draw circle via Skia (stub)."""
        _ = canvas


@dataclass(slots=True)
class Line(Node):
    """Line segment from start to end in local space."""

    x0: float = 0.0
    y0: float = 0.0
    x1: float = 100.0
    y1: float = 0.0
    stroke_color: str = "#FFFFFF"
    stroke_width: float = 2.0

    def draw(self, canvas: Any) -> None:
        """Draw line via Skia (stub)."""
        _ = canvas


@dataclass(slots=True)
class Polygon(Node):
    """Closed polygon from vertex list."""

    vertices: tuple[tuple[float, float], ...] = ()
    fill_color: str = "#FFFFFF"
    stroke_color: str | None = None
    stroke_width: float = 0.0

    def draw(self, canvas: Any) -> None:
        """Draw polygon via Skia (stub)."""
        _ = canvas
