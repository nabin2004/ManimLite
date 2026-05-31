"""Smoke tests until the engine is implemented."""

from __future__ import annotations

import motiongram


def test_version_is_set() -> None:
    assert motiongram.__version__
