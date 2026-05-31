"""Build a single Scene from a SceneSpec."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from motiongram.core import Node, Scene
from motiongram.manifest.errors import ManifestValidationError
from motiongram.manifest.properties import normalize_element_properties
from motiongram.manifest.registry import (
    _resolve_target,
    build_animator,
    instantiate_node,
)
from motiongram.manifest.schema import CanvasSpec, SceneSpec
from motiongram.manifest.time import parse_time
from motiongram.subtitles import SubtitleCue, SubtitleTrack, validate_subtitle_track


@dataclass
class BuiltScene:
    scene: Scene
    node_map: dict[str, Node]
    uses_custom_easing: bool
    voiceover_path: Path | None


def _uses_custom_easing(anim: dict[str, Any]) -> bool:
    if anim.get("easing") is not None:
        return True
    for key in ("animations",):
        children = anim.get(key)
        if isinstance(children, list):
            return any(_uses_custom_easing(c) for c in children if isinstance(c, dict))
    inner = anim.get("animation")
    if isinstance(inner, dict):
        return _uses_custom_easing(inner)
    return False


def _parse_subtitles(
    spec: str | list[dict[str, Any]] | None,
    *,
    base_dir: Path,
    duration: float,
) -> SubtitleTrack | None:
    if spec is None:
        return None
    if isinstance(spec, str):
        from motiongram.subtitles import read_webvtt

        path = (base_dir / spec).resolve()
        if not path.is_file():
            raise ManifestValidationError(f"subtitle file not found: {path}")
        return read_webvtt(path)
    cues: list[SubtitleCue] = []
    for i, raw in enumerate(spec):
        try:
            start = parse_time(raw["start"], field=f"subtitles[{i}].start")
            end = parse_time(raw["end"], field=f"subtitles[{i}].end")
            text = str(raw.get("text", raw.get("typst", "")))
            cues.append(
                SubtitleCue(
                    start=start,
                    end=end,
                    typst=text,
                    plain=str(raw.get("plain", text)),
                    voice=raw.get("voice"),
                )
            )
        except KeyError as exc:
            raise ManifestValidationError(f"subtitle cue[{i}] missing field: {exc}") from exc
    track = SubtitleTrack(cues=tuple(cues))
    issues = validate_subtitle_track(track, duration=duration)
    if issues:
        raise ManifestValidationError("; ".join(issues))
    return track


def build_scene(
    spec: SceneSpec,
    *,
    canvas: CanvasSpec,
    base_dir: Path,
) -> BuiltScene:
    """Materialize one scene from YAML spec."""
    duration = parse_time(spec.duration, field=f"scene[{spec.id}].duration")
    scene_canvas = spec.canvas or canvas
    scene = Scene(
        width=scene_canvas.width,
        height=scene_canvas.height,
        fps=scene_canvas.fps,
        duration=duration,
    )

    if spec.camera and spec.camera.initial:
        init = spec.camera.initial
        if len(init.position) >= 2:
            scene.camera.x = float(init.position[0])
            scene.camera.y = float(init.position[1])
        scene.camera.zoom = float(init.zoom)

    node_map: dict[str, Node] = {}
    uses_easing = False

    for elem in spec.elements:
        if elem.id in node_map:
            raise ManifestValidationError(f"duplicate element id: {elem.id!r}")
        props = normalize_element_properties(dict(elem.properties))
        node = instantiate_node(elem.type, props)
        scene.add_node(node)
        node_map[elem.id] = node

        for anim in elem.animations:
            if _uses_custom_easing(anim):
                uses_easing = True
            start = parse_time(anim["start"], field="animation.start")
            dur = parse_time(anim["duration"], field="animation.duration")
            target = node_map[elem.id]
            animator = build_animator(scene, target, anim, node_map)
            scene.add_animation(start, start + dur, target, animator)

    scene_anims: list[dict[str, Any]] = list(spec.animations)
    if spec.camera:
        scene_anims.extend(spec.camera.animations)

    for anim in scene_anims:
        if _uses_custom_easing(anim):
            uses_easing = True
        start = parse_time(anim["start"], field="animation.start")
        dur = parse_time(anim["duration"], field="animation.duration")
        target = _resolve_target(scene, anim, node_map, default=scene.root)
        animator = build_animator(scene, target, anim, node_map)
        scene.add_animation(start, start + dur, target, animator)

    subtitle_track = _parse_subtitles(spec.subtitles, base_dir=base_dir, duration=duration)
    if subtitle_track is not None:
        scene.subtitle_track = subtitle_track

    voiceover_path: Path | None = None
    if spec.voiceover:
        voiceover_path = (base_dir / spec.voiceover).resolve()
        if not voiceover_path.is_file():
            raise ManifestValidationError(f"voiceover file not found: {voiceover_path}")

    return BuiltScene(
        scene=scene,
        node_map=node_map,
        uses_custom_easing=uses_easing,
        voiceover_path=voiceover_path,
    )
