"""Voice-over defaults and backend wiring."""

from __future__ import annotations

from typmotion import KittenVoiceOverBackend, VoiceOver


def test_voiceover_default_voice_is_jasper() -> None:
    assert VoiceOver(text="hello").voice == "Jasper"


def test_kitten_backend_default_model() -> None:
    assert "kitten-tts" in KittenVoiceOverBackend().model_name
