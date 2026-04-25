# Phase 077 — Mux audio + video

## Goal of this phase

State the design goal: **one container** (MP4) with correctly timestamped A/V streams.

## Problem being solved

“Paste ffmpeg CLI flags” is exactly what this project avoids; muxing is still required—**but** in-process with libav.

## Implementation

Pseudocode:

```text
open container
add video stream (H.264, CFR)
add audio stream (AAC/PCM re-encoded to AAC, common for MP4)
for each video frame: encode + mux with dts/pts
for each audio chunk: encode + mux
write trailer, close
```

## Explanation

**PTS/DTS** handling is the hard part. PyAV abstractions help, but you must still test on VLC + browsers.

## Limitations

Variable frame rate video is harder to mux; CFR first.

## Next phase preview

Phase 078 — A **VoiceOver** hook: text → buffer on the audio timeline.
