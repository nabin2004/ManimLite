# Phase 087 — Scene discovery

## Goal of this phase

Compare patterns: `importlib` the user’s file and ask for a **named** scene vs. convention-based `build_scene()`.

## Problem being solved

`exec(open(...))` is unsafe and brittle. A named attribute lookup after import is the usual compromise.

## Implementation

Sketch:

```python
import importlib.util


def load_module(path: str):
    spec = importlib.util.spec_from_file_location("usermod", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod
```

## Explanation

**Sandboxing** is not provided here; running untrusted user code is its own product concern.

## Limitations

Relative imports inside user scenes may need `sys.path` hacks—document the supported layout.

## Next phase preview

Phase 088 — `RenderConfig` from CLI flags and env **defaults**.
