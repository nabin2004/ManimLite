# Phase 090 — Packaging and lockfile

## Goal of this phase

Tie the tutorial to a **real** project shape: `pyproject.toml` with `hatchling`/`uv`, optional extras, `uv.lock` in git.

## Problem being solved

“Works on my machine” is not acceptable for a team or for CI that must reproduce a render bit-for-bit-ish.

## Implementation

Key ideas only:

```toml
[project]
name = "manimlite"
dependencies = [ "numpy", "av", ... ]

[project.optional-dependencies]
tts = [ "kittentts @ ...", "soundfile" ]
```

```bash
uv lock
uv sync --extra dev
```

## Explanation

**Optional** extras keep the core import path light; heavy TTS/ML does not block classroom installs.

## Limitations

Lockfile PR noise is a cost—worth it for reproducible releases.

## Next phase preview

Phase 091 — **Distribution** choices: PyPI, GitHub releases, Docker later.
