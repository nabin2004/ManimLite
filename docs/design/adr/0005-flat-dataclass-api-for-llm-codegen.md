# ADR-0005: Prefer flat dataclasses and explicit timelines over deep inheritance

- **Status:** Accepted
- **Date:** 2025-04-25

## Context

ManimCE’s inheritance-heavy API is powerful but error-prone for LLM-generated code: implicit state, ordering-sensitive `play()` chains, and large surface area.

## Decision

ManimLite’s public API should favor:

- **`@dataclass` nodes** with explicit fields
- **`Timeline` tuples** instead of implicit animation stacks
- **Small re-export surface** from `manimlite` package

## Consequences

- **Positive:** Easier static analysis; clearer prompts for codegen; fewer hidden globals.
- **Negative:** Some Manim users may find composition more verbose than subclass magic.
- **Follow-up:** Maintain `AGENTS.md` and `api-spec.md` as the contract for humans and LLMs; add CI checks on symbol count / public exports.
