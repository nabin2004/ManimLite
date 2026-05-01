"""Smoke tests until the engine is implemented."""

from __future__ import annotations

import manimlite


def test_version_is_set() -> None:
    assert manimlite.__version__
