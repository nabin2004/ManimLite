# Phase 097 — `AGENTS.md` and LLM codegen

## Goal of this phase

Document **public surface** rules for agents: flat dataclasses, explicit time, no hidden globals, symbol limits.

## Problem being solved

LLMs will produce more working code if the API looks like a **small vocabulary** and consistent patterns (Phase 002).

## Implementation

Point readers to the repo’s [`AGENTS.md`](../AGENTS.md) and [`docs/design/api-spec.md`](../docs/design/api-spec.md) as the contract to prompt against.

## Explanation

A short “agent guide” beats a 50-page manual for first-pass success *if* the API truly stays small (Phase 094 tradeoffs apply).

## Limitations

Benchmarking “80% first-pass” requires a curated prompt set—out of this tutorial’s scope, but the SRS tracks it as NFR-3.

## Next phase preview

Phase 098 — **ManimCE** comparison: what you keep, what you give up (LaTeX parity, 3D, feature breadth).
