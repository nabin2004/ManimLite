"""Tests for multi-scene manifest composition."""

from __future__ import annotations

from pathlib import Path

from motiongram.manifest.loader import render_manifest

ROOT = Path(__file__).resolve().parents[2]
LECTURE = ROOT / "examples/yaml/weight_decay_lecture.yaml"


def test_lecture_sections_and_duration() -> None:
    program, scene = render_manifest(LECTURE)
    # intro + 2 section titles + 2 content scenes
    assert len(program.segments) == 5
    # 4 + 3 + 10 + 3 + 8
    assert scene.duration == 28.0
    assert len(scene.root.children) >= 4


def test_timeline_offsets_merged() -> None:
    program, scene = render_manifest(LECTURE)
    starts = [entry[0] for entry in scene.timeline.entries]
    assert any(s >= 4.0 for s in starts), "animations should be offset past intro scene"
