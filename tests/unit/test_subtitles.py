"""Unit tests for declarative subtitle track (no Skia)."""

from __future__ import annotations

from manimlite.subtitles import (
    SubtitleCue,
    SubtitleStyle,
    SubtitleTrack,
    active_subtitles,
    sort_cues,
    validate_subtitle_track,
    write_webvtt,
)


def test_sort_cues_order() -> None:
    a = SubtitleCue(1.0, 2.0, "b")
    b = SubtitleCue(0.0, 1.0, "a")
    c = SubtitleCue(1.0, 2.0, "a")
    out = sort_cues((a, b, c))
    assert [x.typst for x in out] == ["a", "a", "b"]


def test_active_subtitles_half_open() -> None:
    style = SubtitleStyle()
    t = SubtitleTrack(
        cues=(
            SubtitleCue(0.0, 1.0, "A"),
            SubtitleCue(1.0, 2.0, "B"),
        ),
        style=style,
    )
    assert [x.typst for x in active_subtitles(t, 0.0)] == ["A"]
    assert [x.typst for x in active_subtitles(t, 0.999)] == ["A"]
    assert [x.typst for x in active_subtitles(t, 1.0)] == ["B"]
    assert [x.typst for x in active_subtitles(t, 1.5)] == ["B"]


def test_validate_subtitle_track() -> None:
    track = SubtitleTrack(
        cues=(
            SubtitleCue(-0.1, 1.0, "x"),
            SubtitleCue(0.0, 0.0, "bad"),
            SubtitleCue(0.0, 2.0, "ok"),
        ),
    )
    w = validate_subtitle_track(track, duration=1.5)
    assert any("negative" in x for x in w)
    assert any("need end > start" in x for x in w)
    assert any("past scene duration" in x for x in w)


def test_write_webvtt_only_plain(tmp_path) -> None:
    track = SubtitleTrack(
        cues=(
            SubtitleCue(0.0, 1.0, typst=r"$a$", plain=None),
            SubtitleCue(1.0, 2.0, typst="x", plain="Hello"),
        ),
    )
    p = tmp_path / "c.vtt"
    write_webvtt(track, p)
    body = p.read_text(encoding="utf-8")
    assert "WEBVTT" in body
    assert "Hello" in body
    assert body.count("-->") == 1
    assert "," not in body.split("\n")[2]  # timing line uses . not SRT comma


def test_write_webvtt_timestamp_shape_and_hour(tmp_path) -> None:
    track = SubtitleTrack(
        cues=(
            SubtitleCue(2.0, 4.5, "a", plain="Short form"),
            SubtitleCue(3600.0, 3602.5, "b", plain="With hour"),
        ),
    )
    p = tmp_path / "t.vtt"
    write_webvtt(track, p)
    body = p.read_text(encoding="utf-8")
    assert "00:02.000 --> 00:04.500" in body
    assert "01:00:00.000 --> 01:00:02.500" in body


def test_write_webvtt_voice_and_settings(tmp_path) -> None:
    track = SubtitleTrack(
        cues=(
            SubtitleCue(
                11.0,
                13.0,
                "x",
                plain="We are in New York City",
                voice="Roger Bingham",
                settings="vertical:rl",
            ),
        ),
    )
    p = tmp_path / "v.vtt"
    write_webvtt(track, p)
    body = p.read_text(encoding="utf-8")
    assert "00:11.000 --> 00:13.000 vertical:rl" in body
    assert "<v Roger Bingham>We are in New York City" in body
