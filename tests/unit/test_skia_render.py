"""Skia frame output: RGBA ndarray shape and deterministic width/height."""

from __future__ import annotations

from typmotion.core import Circle, Scene
from typmotion.render import SkiaCanvas, SkiaRenderer


def test_skia_render_frame_returns_rgba_numpy() -> None:
    scene = Scene(width=32, height=24, fps=30.0)
    scene.add_node(Circle(x=10, y=8, r=3, progress=1.0, ch="@"))
    r = SkiaRenderer()
    frame = r.render_frame(scene, 0.0)
    assert frame.shape == (24, 32, 4)
    assert frame.dtype == "uint8"
    # Center ring should brighten vs background (mostly black clear)
    assert frame[..., :3].sum() > 0


def test_skia_canvas_optional_methods_exist() -> None:
    import skia

    surface = skia.Surface(16, 16)
    c = SkiaCanvas(surface)
    assert hasattr(c, "stroke_line")
    assert hasattr(c, "fill_polygon")
    c.set_pixel(4, 4, "#")
    c.stroke_line(0, 0, 15, 15, "#FFFFFF", 1.0)
    c.fill_polygon(
        ((1, 1), (14, 1), (8, 14)),
        fill_color="#FF0000",
        stroke_color=None,
        stroke_width=0.0,
        ox=0.0,
        oy=0.0,
    )
