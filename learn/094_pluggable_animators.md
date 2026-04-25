# Phase 094 — Pluggable animators

## Goal of this phase

Treat animators as **data + apply function** registered by name, or as plain callables in user code.

## Problem being solved

A closed list of `Move`/`Fade` is too small; an open `exec` of strings is too unsafe. Middle ground: **register** small dataclass animators with stable schemas.

## Implementation

```python
ANIM: dict[str, type] = {}


def anim(name: str):
    def deco(cls: type) -> type:
        ANIM[name] = cls
        return cls
    return deco


@anim("move")
class Move: ...
```

## Explanation

**Schema stability** (fields, defaults) is what makes LLM codegen work—better than “freeform Python lambda.”

## Limitations

Plugins can collide on names; namespaces (`pkg_move`) or priorities help.

## Next phase preview

Phase 095 — Pluggable **voice-over** backends: Kitten, baked WAV, cloud later with the same `VoiceOverBackend`.
