"""Tests for procedural manifest materialization (`manimlite.procedural`)."""

from __future__ import annotations

from manimlite import Scene, world_shell
from manimlite.procedural import (
    apply_rainy_landscape_animations,
    default_rainy_landscape_manifest,
    materialize_rainy_landscape,
)
from manimlite.world import WorldSpec


def test_default_rainy_landscape_handles_shape() -> None:
    spec = WorldSpec(world_width=10.0, ground_y=2.5)
    manifest = default_rainy_landscape_manifest()

    handles = materialize_rainy_landscape(world_shell(), spec, manifest)
    assert len(handles.clouds) == len(manifest.clouds)
    assert len(handles.rain) == manifest.rain.waves * manifest.rain.drops_per_wave


def test_rain_placement_is_seed_deterministic() -> None:
    spec = WorldSpec(world_width=10.0, ground_y=2.5)
    manifest = default_rainy_landscape_manifest()

    def rain_tuple(h: object) -> tuple[tuple[float, float, float, float], ...]:
        hh = getattr(h, "rain")
        return tuple((drop.x, y0, y1, start_t) for drop, y0, y1, start_t in hh)

    h1 = materialize_rainy_landscape(world_shell(), spec, manifest)
    h2 = materialize_rainy_landscape(world_shell(), spec, manifest)
    assert rain_tuple(h1) == rain_tuple(h2)


def test_apply_landscape_animation_entry_count_matches_clouds_and_valid_rain() -> None:
    duration = 15.0
    spec = WorldSpec(world_width=10.0, ground_y=2.5)
    manifest = default_rainy_landscape_manifest()
    handles = materialize_rainy_landscape(world_shell(), spec, manifest)

    scene = Scene(duration=duration)
    apply_rainy_landscape_animations(scene, duration=duration, manifest=manifest, handles=handles)

    anim = manifest.animation
    valid_rain = 0
    for idx, (_, _, _, start_t) in enumerate(handles.rain):
        mod = idx % anim.rain_duration_period
        dur = anim.rain_duration_base + mod * anim.rain_duration_stride
        t0 = max(0.0, min(start_t, duration - 0.08))
        t1 = min(t0 + dur, duration)
        if t1 - t0 >= 0.1:
            valid_rain += 1

    assert len(scene.timeline.entries) == len(handles.clouds) + valid_rain
