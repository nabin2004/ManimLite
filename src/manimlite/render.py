"""Skia-backed frame rendering (scene graph + timeline, then rasterize)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

import numpy as np
import numpy.typing as npt

from manimlite.core import Scene
from manimlite.engine import step_frame

if TYPE_CHECKING:
    import skia


def _hex_to_color(s: str) -> int:
    h = s.strip().lstrip("#")
    if len(h) == 6:
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    else:
        r, g, b = 255, 255, 255
    import skia as _skia

    return cast(int, _skia.Color(r, g, b, 255))


class SkiaCanvas:
    """Maps ``Canvas.set_pixel`` to Skia fills; optional vector hooks for lines/polygons."""

    __slots__ = ("_canvas", "_paint")

    def __init__(self, surface: skia.Surface) -> None:
        import skia

        self._canvas = surface.getCanvas()
        self._paint = skia.Paint()
        self._paint.setAntiAlias(True)

    def set_pixel(self, x: int, y: int, ch: str = "#") -> None:
        import skia

        self._paint.setStyle(skia.Paint.kFill_Style)
        self._paint.setColor(skia.ColorWHITE)
        _ = ch  # ASCII token; future: map to palette
        rect = skia.Rect(float(x), float(y), float(x + 1), float(y + 1))
        self._canvas.drawRect(rect, self._paint)

    def stroke_line(
        self,
        x0: float,
        y0: float,
        x1: float,
        y1: float,
        color: str,
        width: float,
    ) -> None:
        import skia

        self._paint.setStrokeWidth(max(width, 0.001))
        self._paint.setStyle(skia.Paint.kStroke_Style)
        self._paint.setColor(_hex_to_color(color))
        p = skia.Path()
        p.moveTo(x0, y0)
        p.lineTo(x1, y1)
        self._canvas.drawPath(p, self._paint)

    def fill_polygon(
        self,
        points: tuple[tuple[float, float], ...],
        *,
        fill_color: str,
        stroke_color: str | None,
        stroke_width: float,
        ox: float,
        oy: float,
    ) -> None:
        import skia

        if len(points) < 2:
            return
        pth = skia.Path()
        pth.moveTo(ox + points[0][0], oy + points[0][1])
        for vx, vy in points[1:]:
            pth.lineTo(ox + vx, oy + vy)
        pth.close()

        fill = skia.Paint()
        fill.setAntiAlias(True)
        fill.setStyle(skia.Paint.kFill_Style)
        fill.setColor(_hex_to_color(fill_color))
        self._canvas.drawPath(pth, fill)

        if stroke_color is not None and stroke_width > 0.0:
            outline = skia.Paint()
            outline.setAntiAlias(True)
            outline.setStyle(skia.Paint.kStroke_Style)
            outline.setStrokeWidth(stroke_width)
            outline.setColor(_hex_to_color(stroke_color))
            self._canvas.drawPath(pth, outline)

    def draw_svg_bytes(self, data: bytes, ox: float, oy: float, scale: float = 1.0) -> None:
        """Rasterize SVG (e.g. Typst output) into local coordinates."""

        import skia

        stream = skia.MemoryStream(data)
        dom = skia.SVGDOM.MakeFromStream(stream)
        if dom is None:
            return
        self._canvas.save()
        self._canvas.translate(ox, oy)
        self._canvas.scale(scale, scale)
        dom.render(self._canvas)
        self._canvas.restore()


@dataclass(slots=True)
class SkiaRenderer:
    """Rasterize the scene at time ``t``; returns HxWx4 ``uint8`` RGBA."""

    clear_color: tuple[int, int, int] = (0, 0, 0)

    def render_frame(self, scene: Scene, t: float) -> npt.NDArray[np.uint8]:
        import skia

        surface = skia.Surface(scene.width, scene.height)
        r, g, b = self.clear_color
        surface.getCanvas().clear(skia.Color(r, g, b, 255))

        dt = 1.0 / scene.fps if scene.fps > 0 else 1.0 / 30.0
        step_frame(scene, t, dt)

        canvas = SkiaCanvas(surface)
        scene.root.draw(canvas, 0.0, 0.0)

        img = surface.makeImageSnapshot()
        return np.asarray(img)
