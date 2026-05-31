# Typst subtitles in MotionGram

Burned-in captions are **declarative**: you attach a `SubtitleTrack` to `Scene.subtitle_track`. The Skia renderer draws cues **after** the camera transform, so text stays fixed on screen during pans and zooms.

## Dependencies

- The **Typst CLI** must be on `PATH` (same as `MathExpr`).
- SVG output is cached under `~/.cache/motiongram/typst` or `MOTIONGRAM_CACHE_HOME/typst`.

## Required shape (for humans and LLM agents)

1. Build a tuple of `SubtitleCue(start, end, typst=..., plain=...)`.
2. Wrap them in `SubtitleTrack(cues=(...), style=SubtitleStyle(...))`.
3. Assign `scene.subtitle_track = track` (or pass `subtitle_track=` into `Scene(...)`).
4. Optionally call `validate_subtitle_track(track, duration=scene.duration)` and log warnings.

Example (conceptual):

```python
from motiongram import Scene, SubtitleCue, SubtitleStyle, SubtitleTrack, validate_subtitle_track

scene = Scene(width=1280, height=720, fps=30.0, duration=5.0)
scene.subtitle_track = SubtitleTrack(
    style=SubtitleStyle(font_size=22.0, color="#FFFFFF", bottom_margin=48.0),
    cues=(
        SubtitleCue(
            0.0,
            2.0,
            typst='We sketch $x^2 + y^2 = r^2$ for a circle.',
            plain="We sketch x squared plus y squared equals r squared for a circle.",
        ),
        SubtitleCue(
            2.0,
            4.5,
            typst="The Pythagorean theorem links the sides.",
            plain="The Pythagorean theorem links the sides.",
        ),
    ),
)
for w in validate_subtitle_track(scene.subtitle_track, duration=scene.duration):
    print("subtitle:", w)
```

## Time and FPS

- **Half-open window:** a cue is shown when `start <= t < end` (seconds).
- This avoids two consecutive cues both appearing on the exact `end == start` boundary frame.
- Frame times are quantized by `SkiaRenderer` / `PyAVEncoder` to multiples of `1/fps`. Keep `start`/`end` on frame boundaries when you care about tight cuts.

## Typst body rules

- **No LaTeX.** Use Typst math: inline `$...$`, display `[$ ... $]` if you need a full document with `#set page` (advanced).
- **Default wrapper:** if `typst` does *not* start with `#set` or `#page`, MotionGram wraps your fragment in a centered paragraph with page width and text size derived from `SubtitleStyle` and scene width.

- **Transparent compositing:** the default wrapper sets Typst `page(fill: none)` so glyphs composite on your scene background—avoiding a solid white page that washes out light ink colors.
- **`#` starts markup** in Typst. Literal text that looks like code may need escaping or string syntax per Typst rules.
- **Brackets:** unbalanced `[` / `]` inside fragments can break the wrapper. For full control, supply a **whole document** whose first line begins with `#set page` or `#page` (pass-through mode; you own layout and margins).

## Layout (`SubtitleStyle`)

- `font_size` — same nominal units as `Text.font_size` (Skia pixels); converted to Typst points for compilation.
- `max_width_ratio` — fraction of scene width used as Typst page width (line wrapping).
- `bottom_margin` — space from the **bottom** of the frame to the lowest subtitle block.
- `line_gap` — vertical gap between stacked cues when multiple cues overlap in time.

Stacking order: cues are sorted by start, end, typst, then plain / WebVTT fields for ties. The first in that order is drawn **closest to the bottom**; additional overlapping cues stack **upward**.

## WebVTT sidecar

MotionGram writes **WebVTT**, not SubRip (SRT): timestamps use a **period** before milliseconds (`00:11.000`), not a comma. When the cue lies in the first hour, times use the compact **`MM:SS.mmm`** form; longer clips use **`HH:MM:SS.mmm`**.

Optional on each `SubtitleCue` (WebVTT-only; ignored for burned-in Typst):

- **`voice=...`** — emits a voice span: ``<v Speaker Name>`` before the payload line (unsafe characters in the name are stripped).
- **`settings=...`** — appended on the **same line** as the timing arrow after a space (e.g. ``vertical:rl``, `line:90%`); pass a single string of WebVTT cue settings.

- `write_webvtt(track, path)` writes cues that have a non-empty `plain` string.
- There is **no** automatic conversion from Typst to plain text. Agents should fill `plain` with a sensible accessibility line when VTT output is required.

## Failure modes

- **`typst` missing:** subtitles are skipped; one warning may be printed to stderr per process.
- **Compile error:** the cache step removes incomplete files; that cue simply does not render (same family of behavior as failed `MathExpr` cache).
- **Empty `typst`:** cue is skipped.

## Anti-patterns

- Using many `Text` nodes and timeline fades for every caption when you need **screen-fixed** text during camera motion—use `subtitle_track` instead.
- Putting long narration-only strings in `typst` without testing Typst syntax—validate with a short render early.

## See also

- [api-spec.md](../design/api-spec.md) — contract summary
- [AGENTS.md](../../AGENTS.md) — authoring rules for tools
