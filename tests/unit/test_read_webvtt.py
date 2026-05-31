"""Tests for WebVTT reader."""

from __future__ import annotations

from motiongram.subtitles import read_webvtt, write_webvtt, SubtitleCue, SubtitleTrack


def test_read_write_webvtt_roundtrip(tmp_path) -> None:
    track = SubtitleTrack(
        cues=(
            SubtitleCue(0.0, 2.0, typst="Hello", plain="Hello"),
            SubtitleCue(2.5, 4.0, typst="World", plain="World", voice="Narrator"),
        )
    )
    path = tmp_path / "test.vtt"
    write_webvtt(track, path)
    loaded = read_webvtt(path)
    assert len(loaded.cues) == 2
    assert loaded.cues[0].plain == "Hello"
    assert loaded.cues[1].voice == "Narrator"
    assert abs(loaded.cues[1].start - 2.5) < 1e-6
