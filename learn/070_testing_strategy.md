# Phase 070 — Testing strategy

## Goal of this phase

Define what to test in a **graphics** engine without flapping float noise everywhere.

## Problem being solved

“Snapshot the whole video” is slow and platform-sensitive. The right mix is small unit tests + a few goldens.

## Implementation

| Layer | Test kind | Why |
|-------|-----------|-----|
| Easing, lerp, time mapping | `pytest` + tables | pure math |
| Transform compose | `pytest` | algebraic |
| Scene graph order | `pytest` | deterministic |
| Raster output | small canvas hash (CRC32 of bytes) or pixel spot-checks | short + stable on one platform |
| PyAV | optional integration, nightly | heavy deps |
| TTS | mock backend, optional smoke | network/GPU |

## Explanation

**Golden image tests** should use tiny resolutions (e.g. 32×24) to keep diffs readable.

## Limitations

Skia/AA may differ by minor versions; pin versions in goldens or compare tolerance carefully.

## Next phase preview

Phase 071 — **Architecture recap** before performance and packaging chapters.
