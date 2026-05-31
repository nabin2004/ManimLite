"""Principle: Typst subtitles — declarative cues, screen-fixed over the camera.

Brand ink (#1E1E1E) canvas with cyan / crimson accents (aligned with ``showcase_intro``).

Run::

    python examples/principles/27_subtitles_typst.py

Requires: skia-python, typst on PATH.
"""

from __future__ import annotations

import sys
from pathlib import Path

from motiongram import (
    CameraPan,
    Circle,
    CircleOutline,
    Scene,
    SkiaRenderer,
    SubtitleCue,
    SubtitleStyle,
    SubtitleTrack,
    validate_subtitle_track,
    write_webvtt,
)
from motiongram.export import PyAVEncoder

# Match showcase_intro reel palette
WIDTH = 1280
HEIGHT = 720
FPS = 30.0
DURATION = 4.0

BG = (30, 30, 30)  # #1E1E1E brand ink
C_ACCENT_COOL = "#5DD2E8"
C_ACCENT_WARM = "#A51C30"
C_TITLE = "#EDF1FA"


def build_scene() -> Scene:
    scene = Scene(width=WIDTH, height=HEIGHT, fps=FPS, duration=DURATION)
    disk = Circle(
        x=WIDTH // 2,
        y=HEIGHT // 2,
        r=120,
        progress=0.0,
        fill_color="#2E2E2E",
        stroke_color=C_ACCENT_WARM,
        stroke_width=2.5,
    )
    scene.add_node(disk)
    scene.add_animation(0.0, DURATION, disk, CircleOutline())
    scene.add_animation(
        0.0,
        DURATION,
        scene.root,
        CameraPan(
            scene,
            x0=WIDTH / 2,
            y0=HEIGHT / 2,
            x1=WIDTH / 2 + 160,
            y1=HEIGHT / 2,
        ),
    )

    scene.subtitle_track = SubtitleTrack(
        style=SubtitleStyle(
            font_size=26.0,
            color=C_TITLE,
            bottom_margin=52.0,
            max_width_ratio=0.88,
            line_gap=10.0,
        ),
        cues=(
            SubtitleCue(
                0.0,
                2.0,
                typst="Area of a disk: $A = pi r^2$.",
                plain="Area of a disk: A equals pi r squared.",
                voice="Narrator",
            ),
            SubtitleCue(
                2.0,
                4.0,
                typst=(
                    f"Screen-fixed captions on brand ink — "
                    f"#text(fill: rgb(\"{C_ACCENT_COOL}\"))[cyan] ring energy, "
                    f"#text(fill: rgb(\"{C_ACCENT_WARM}\"))[crimson] stroke."
                ),
                plain=(
                    "Screen-fixed captions on brand ink: cyan ring, crimson stroke "
                    "(showcase_intro palette)."
                ),
                voice="Narrator",
                settings="vertical:rl",
            ),
        ),
    )
    for msg in validate_subtitle_track(scene.subtitle_track, duration=DURATION):
        print("subtitle warning:", msg, file=sys.stderr)

    return scene


def get_skia_renderer() -> SkiaRenderer:
    return SkiaRenderer(clear_color=BG)


def main() -> None:
    scene = build_scene()
    out = Path(__file__).with_suffix(".mp4")
    vtt = Path(__file__).with_suffix(".vtt")
    write_webvtt(scene.subtitle_track, vtt, scene_duration=DURATION)
    print(f"WebVTT: {vtt}", file=sys.stderr)
    encoder = PyAVEncoder(scene=scene, output_path=out, renderer=get_skia_renderer())
    result = encoder.encode(verbose=True)
    print(f"Output: {result}", file=sys.stderr)


if __name__ == "__main__":
    main()
