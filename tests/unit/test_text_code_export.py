"""Tests for Text rendering, CodeBlock rendering, and PyAVEncoder."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from typmotion.animate import CircleOutline, MoveX
from typmotion.core import Circle, Scene
from typmotion.render import SkiaCanvas, SkiaRenderer
from typmotion.text import CodeBlock, Text


def test_text_draw_produces_ink() -> None:
    scene = Scene(width=200, height=60, fps=30.0)
    scene.add_node(Text(content="Hello Typmotion", x=10, y=5, font_size=20.0))
    frame = SkiaRenderer().render_frame(scene, 0.0)
    assert frame.shape == (60, 200, 4)
    assert frame[..., :3].astype("int64").sum() > 0


def test_text_empty_content_no_crash() -> None:
    scene = Scene(width=64, height=32, fps=30.0)
    scene.add_node(Text(content="", x=0, y=0))
    frame = SkiaRenderer().render_frame(scene, 0.0)
    assert frame.shape == (32, 64, 4)


def test_text_custom_color() -> None:
    scene = Scene(width=200, height=60, fps=30.0)
    scene.add_node(Text(content="Red", x=10, y=5, font_size=20.0, color="#FF0000"))
    frame = SkiaRenderer().render_frame(scene, 0.0)
    assert frame[..., :3].astype("int64").sum() > 0


def test_codeblock_draw_produces_ink() -> None:
    scene = Scene(width=400, height=100, fps=30.0)
    scene.add_node(
        CodeBlock(code="def f(x):\n    return x + 1", x=10, y=10, font_size=14.0)
    )
    frame = SkiaRenderer().render_frame(scene, 0.0)
    assert frame.shape == (100, 400, 4)
    assert frame[..., :3].astype("int64").sum() > 0


def test_codeblock_empty_code_no_crash() -> None:
    scene = Scene(width=64, height=32, fps=30.0)
    scene.add_node(CodeBlock(code="", x=0, y=0))
    frame = SkiaRenderer().render_frame(scene, 0.0)
    assert frame.shape == (32, 64, 4)


def test_pyav_encoder_produces_mp4(tmp_path: Path) -> None:
    from typmotion.export import PyAVEncoder

    scene = Scene(width=160, height=120, fps=10.0, duration=0.5)
    c = Circle(x=80, y=60, r=30, progress=0.0)
    scene.add_node(c)
    scene.add_animation(0.0, 0.5, c, CircleOutline())

    out = tmp_path / "test_output.mp4"
    enc = PyAVEncoder(scene=scene, output_path=out)
    result = enc.encode(verbose=False)
    assert result.is_file()
    assert result.stat().st_size > 100


def test_pyav_encoder_with_text(tmp_path: Path) -> None:
    from typmotion.export import PyAVEncoder

    scene = Scene(width=320, height=240, fps=10.0, duration=0.5)
    t = Text(content="Encode me", x=20, y=20, font_size=24.0)
    scene.add_node(t)
    scene.add_animation(0.0, 0.5, t, MoveX(20.0, 200.0))

    out = tmp_path / "text_output.mp4"
    enc = PyAVEncoder(scene=scene, output_path=out)
    result = enc.encode(verbose=False)
    assert result.is_file()
    assert result.stat().st_size > 100


def test_skia_canvas_draw_text_method() -> None:
    import skia

    surface = skia.Surface(100, 50)
    canvas = SkiaCanvas(surface)
    canvas.draw_text("Hi", 5.0, 5.0, 14.0, "#FFFFFF")
    arr = np.asarray(surface.makeImageSnapshot())
    assert arr[..., :3].astype("int64").sum() > 0
