# Phase 096 — CI and tests

## Goal of this phase

Split CI: **fast** (lint+types+unit) on every commit; **slow** (encode smoke) on nightly or main.

## Problem being solved

A 20-minute job on every push kills contribution velocity; **no** tests kills reliability.

## Implementation

```yaml
# .github/workflows/ci.yml (concept)
jobs:
  fast: [ruff, mypy, pytest -m "not slow"]
  slow: [pytest -m slow]  # on schedule
```

## Explanation

Mark tests with `@pytest.mark.slow` and default `pytest` to skip them in dev unless `-m slow`.

## Limitations

Runner disk and codec availability; keep golden tests tiny.

## Next phase preview

Phase 097 — [`AGENTS.md`](../AGENTS.md) and LLM codegen rules.
