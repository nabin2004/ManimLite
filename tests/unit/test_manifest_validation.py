"""Tests for manifest validation errors."""

from __future__ import annotations

import pytest

from motiongram.manifest.errors import ManifestValidationError
from motiongram.manifest.loader import load_manifest
from motiongram.manifest.registry import instantiate_node


def test_unknown_component_type() -> None:
    with pytest.raises(ManifestValidationError, match="unknown component type"):
        instantiate_node("NotARealComponent", {})


def test_empty_manifest_rejected(tmp_path) -> None:
    path = tmp_path / "empty.yaml"
    path.write_text('version: "1.0"\n', encoding="utf-8")
    with pytest.raises(ManifestValidationError):
        load_manifest(path)


def test_latex_property_rejected() -> None:
    with pytest.raises(ManifestValidationError, match="Typst"):
        from motiongram.manifest.properties import normalize_element_properties

        normalize_element_properties({"latex": "x^2"})
