"""Tests for building scenes from YAML manifests."""

from __future__ import annotations

from pathlib import Path

from motiongram.animate import apply_timeline
from motiongram.manifest.loader import render_manifest

ROOT = Path(__file__).resolve().parents[2]
SHOWCASE = ROOT / "examples/yaml/deeplearning_showcase.yaml"


def test_deeplearning_showcase_build() -> None:
    program, scene = render_manifest(SHOWCASE)
    assert len(program.segments) == 1
    assert scene.duration == 8.0
    assert len(scene.root.children) == 4
    assert len(scene.timeline.entries) == 5

    weights = scene.root.children[0]
    apply_timeline(scene, 4.0, ease=None)
    assert weights.highlight_row == 2  # type: ignore[attr-defined]

    net = scene.root.children[1]
    apply_timeline(scene, 8.0, ease=None)
    assert net.progress == 1.0  # type: ignore[attr-defined]
