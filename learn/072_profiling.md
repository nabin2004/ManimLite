# Phase 072 — Profiling

## Goal of this phase

Use `cProfile` or `py-spy` to see whether time is in **raster**, **encode**, or **I/O**—not guess.

## Problem being solved

Optimizing the wrong layer (“rewrite easing in C”) while PNG export dominates is a classic mistake.

## Implementation

```bash
# python -m cProfile -o out.prof your_scene.py
# snakeviz out.prof   # optional
```

```python
import cProfile
import pstats
from pstats import SortKey

# pr = cProfile.Profile()
# pr.runctx("export()", globals(), locals())
# pr.dump_stats("out.prof")
```

## Explanation

Target metrics from Phase 001: time-to-first-frame, encode throughput (fps of encoding), and peak RSS.

## Limitations

Profiling in CI is noisy; run locally on a quiet machine, fixed CPU governor when possible.

## Next phase preview

Phase 073 — Reiterate why **disk frame stores** are off the hot path.
