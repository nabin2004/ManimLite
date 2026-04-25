# Phase 086 — CLI `render`

## Goal of this phase

Sketch the CLI surface: input path, optional scene symbol, config overrides, output path.

## Problem being solved

`python -c` is not a user interface; educators need a command they can paste into notes.

## Implementation

```text
manimlite render myscene.py --scene MyScene -o out.mp4 -r 30 -s 5
```

`Typer` or `argparse` both work; keep flags explicit (LLM-friendlier than env vars).

## Explanation

**Discovery** of `Scene` objects is the tricky bit—see Phase 087.

## Limitations

Shell escaping on Windows; keep paths in quotes in docs.

## Next phase preview

Phase 087 — **Import** user modules safely, find subclasses or registry entries.
