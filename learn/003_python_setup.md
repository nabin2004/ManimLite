# Phase 003 — Python / uv setup

## Goal of this phase

Standardize the **tooling** for the tutorial: Python 3.11+, a virtual environment, and a single-file workflow for early toy code.

## Problem being solved

If every phase needs different install steps, readers drop out. Early phases should run with **stdlib + print** only.

## Implementation

Use a venv and run files directly.

```bash
# from repo root (illustrative)
python3.11 -m venv .venv
source .venv/bin/activate
python learn/toy/phase005.py   # later phases add toy/ scripts if you create them
```

For the first 10 phases, you can paste code into `python -` or a file `toy.py`.

```python
# toy.py — minimal sanity check (Phase 003)
from __future__ import annotations

import sys

assert sys.version_info >= (3, 11), "Use Python 3.11+"
print("ok", sys.version.split()[0])
```

## Explanation

We use 3.11+ for **better error messages**, `slots` on dataclasses later, and modern typing. The real `Typmotion` repo uses `uv`; for learning, plain venv is enough.

## Limitations

No packaging yet—`pyproject.toml` appears in Phase 090 when the project shape matters.

## Next phase preview

Phase 004 — Canvas and coordinates: origin, axes, and pixel addressing for the ASCII screen.
