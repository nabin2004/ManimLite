"""Tests for recipe expansion."""

from __future__ import annotations

from pathlib import Path

from motiongram.manifest.loader import load_and_compose
from motiongram.manifest.compose import merge_to_single_scene

ROOT = Path(__file__).resolve().parents[2]
LECTURE = ROOT / "examples/yaml/weight_decay_lecture.yaml"


def test_forward_pass_recipe_adds_animations() -> None:
    program = load_and_compose(LECTURE)
    forward_segment = next(s for s in program.segments if s.scene_spec.id == "forward_pass_demo")
    recipe_entries = [
        e for e in forward_segment.built.scene.timeline.entries
    ]
    assert len(recipe_entries) == 3
    assert recipe_entries[0][0] == 1.0
    assert recipe_entries[-1][1] == 7.0
