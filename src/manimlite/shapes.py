"""Vector primitives: lines and polygons (:class:`~manimlite.core.Circle` is canonical)."""

from __future__ import annotations

from dataclasses import dataclass

from manimlite.canvas import Canvas

# Canonical circle (grid + upcoming vector backends) lives in ``core``.
from manimlite.core import Circle, Node  # Circle: canonical (see core)


@dataclass(slots=True)
class Line(Node):
    """Line segment from start to end in local space.

    Because :class:`Line` subclasses :class:`~manimlite.core.Node`, positional
    arguments bind *Node* fields ``x``, ``y``, and ``children`` — use keyword
    arguments for ``x0`` … ``y1`` (e.g. ``Line(x0=0, y0=0, x1=1, y1=1)``).
    """

    x0: float = 0.0
    y0: float = 0.0
    x1: float = 100.0
    y1: float = 0.0
    stroke_color: str = "#FFFFFF"
    stroke_width: float = 2.0

    def draw(self, canvas: Canvas, ox: float = 0.0, oy: float = 0.0) -> None:
        px = ox + self.x
        py = oy + self.y
        stroke_line = getattr(canvas, "stroke_line", None)
        if stroke_line is not None:
            stroke_line(
                px + self.x0,
                py + self.y0,
                px + self.x1,
                py + self.y1,
                self.stroke_color,
                self.stroke_width,
            )
        Node.draw(self, canvas, ox, oy)


@dataclass(slots=True)
class Polygon(Node):
    """Closed polygon from vertex list."""

    vertices: tuple[tuple[float, float], ...] = ()
    fill_color: str = "#FFFFFF"
    stroke_color: str | None = None
    stroke_width: float = 0.0

    def draw(self, canvas: Canvas, ox: float = 0.0, oy: float = 0.0) -> None:
        px = ox + self.x
        py = oy + self.y
        fill_polygon = getattr(canvas, "fill_polygon", None)
        if fill_polygon is not None and len(self.vertices) >= 3:
            fill_polygon(
                self.vertices,
                fill_color=self.fill_color,
                stroke_color=self.stroke_color,
                stroke_width=self.stroke_width,
                ox=px,
                oy=py,
            )
        Node.draw(self, canvas, ox, oy)


__all__ = ["Circle", "Line", "Polygon"]
