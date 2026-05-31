"""Tests for manifest time parsing."""

from __future__ import annotations

import pytest

from motiongram.manifest.errors import ManifestValidationError
from motiongram.manifest.time import parse_time


def test_parse_time_number() -> None:
    assert parse_time(12) == 12.0
    assert parse_time(0.5) == 0.5


def test_parse_time_string_seconds() -> None:
    assert parse_time("12s") == 12.0
    assert parse_time("0.5s") == 0.5
    assert parse_time("8") == 8.0


def test_parse_time_invalid() -> None:
    with pytest.raises(ManifestValidationError):
        parse_time("not-a-time")
    with pytest.raises(ManifestValidationError):
        parse_time(True)
