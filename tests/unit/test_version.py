"""Smoke tests until the engine is implemented."""

from __future__ import annotations

import typmotion


def test_version_is_set() -> None:
    assert typmotion.__version__
