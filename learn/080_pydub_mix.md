# Phase 080 — pydub mix (sketch)

## Goal of this phase

Overlay narration + background music: **amplitude** and **offset** in time, export to a unified PCM for muxing.

## Problem being solved

Each clip may have different sample rates; mixing normalizes to one rate before the encoder.

## Implementation

```python
# pip install pydub
# from pydub import AudioSegment
# bg = AudioSegment.from_file("bgm.mp3")
# vo = AudioSegment(data=wav_bytes, format="wav")
# mixed = bg.overlay(vo, position=int(t0*1000))
# mixed = mixed.set_frame_rate(48000).set_channels(1)  # example
```

## Explanation

`pydub` often leans on **ffmpeg** for decoding exotic formats. That is *decode*, not the **video** encode path—acceptable if isolated and optional.

## Limitations

For strict “no ffmpeg binary anywhere,” restrict inputs to **WAV/PCM** and implement decode-free mixing.

## Next phase preview

Phase 081 — **Typst** math cache concept: hash expr → SVG bytes.
