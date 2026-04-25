# Phase 092 — Plugin shapes

## Goal of this phase

Allow third-party packages to register new drawables: `manimlite.plugins` entry points or a simple `register_shape("heart", factory)`.

## Problem being solved

Forking the core for every new primitive does not scale.

## Implementation

Sketch:

```python
SHAPE_REGISTRY: dict[str, type] = {}


def register(name: str, cls: type) -> None:
    SHAPE_REGISTRY[name] = cls
```

`importlib.metadata.entry_points` can populate this at import time.

## Explanation

**Registry** is LLM-friendlier than import-time side-effect magic, but both exist in the wild—pick one and document it.

## Limitations

Security: loading plugins runs arbitrary code; same caveats as user scenes.

## Next phase preview

Phase 093 — Pluggable **renderers** (numpy vs skia) selected by `RenderConfig`.
