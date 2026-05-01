"""Typst compile cache + MathExpr integration (skipped when ``typst`` CLI is absent)."""

from __future__ import annotations

import shutil

import pytest

from manimlite.core import Scene
from manimlite.render import SkiaRenderer
from manimlite.text import MathExpr
from manimlite.typst_cache import cached_typst_svg_path, typst_cache_key


def test_typst_cache_key_stable() -> None:
    assert typst_cache_key("integral") == typst_cache_key("integral")


def test_cached_typst_requires_cli() -> None:
    if shutil.which("typst") is None:
        assert cached_typst_svg_path("alpha + beta") is None


@pytest.mark.skipif(shutil.which("typst") is None, reason="typst binary not installed")
def test_math_expr_skia_frame_has_ink() -> None:
    scene = Scene(width=160, height=96, fps=30.0)
    scene.add_node(MathExpr(typst_source="sum_(i=0)^n i", x=12.0, y=20.0))
    buf = SkiaRenderer().render_frame(scene, 0.0)
    assert buf.shape == (96, 160, 4)
    assert buf[..., :3].astype("int64").sum() > 800
