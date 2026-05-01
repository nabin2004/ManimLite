# Phase 079 — Kitten TTS (optional)

## Goal of this phase

Map the ManimLite repo’s **optional** `[tts]` story to the tutorial: local synthesis without cloud keys.

## Problem being solved

Piper (GPL) vs **Kitten TTS (Apache-2.0)** license fit matters for MIT cores; keep TTS out of the default install if size matters.

## Implementation

`VoiceOver` remains backend-agnostic. A `KittenVoiceOverBackend` (see repo `src/manimlite/audio/voiceover.py`) wraps the upstream wheel.

**Do not** import TTS in core animation tests; mock bytes in unit tests.

## Explanation

Kitten is **developer preview**; pin versions and call out that upstream may bring large transitive dependencies.

## Limitations

Air-gapped builds need a model cache plan (HF or vendored files).

## Next phase preview

Phase 080 — `pydub` for **mixing** short clips; mention ffmpeg as an *optional* helper for weird formats, not the video encode path.
