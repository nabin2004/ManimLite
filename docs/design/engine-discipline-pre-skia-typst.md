# Engine discipline before Skia / Typst

> **You are at the point where you should stop adding features blindly and start enforcing architecture discipline.**
>
> This document is a practical map: current state, the invariant to reach before new render stacks, **litmus tests** (non-negotiable checkpoints), phased TODOs, and the order of work so Skia and Typst stay in the right layers.

---

## Table of contents

1. [Current state (honest map)](#1-current-state-honest-map)
2. [The real goal before Skia / Typst](#2-the-real-goal-before-skia--typst)
3. [Litmus tests (non-negotiable checkpoints)](#3-litmus-tests-non-negotiable-checkpoints)
4. [TODOs before Skia / Typst](#4-todos-before-skia--typst)
5. [Only after all of that → Skia](#5-only-after-all-of-that--skia)
6. [Only after Skia → Typst](#6-only-after-skia--typst)
7. [Final mental model](#7-final-mental-model-three-layers)
8. [If you follow the wrong order](#8-if-you-follow-the-wrong-order)
9. [TL;DR](#tldr)

---

## 1. Current state (honest map)

You already have:

### Core system

- Scene graph (`Node`)
- Renderer loop (`play`)
- Timeline system
- Animators (`MoveX`, `CircleOutline`)
- Basic composition (`Scene.add_animation`)

### Output layer

- ASCII renderer (terminal grid)

### Animation model (hybrid)

- Procedural animators
- Timeline scheduling
- Manual `progress` hacks (still leaking in)

---

## 2. The real goal before Skia / Typst

Before you touch **Skia** or **Typst**, you need this invariant:

> **No visual behavior depends on renderer implementation.**

Right now, you are still slightly coupled to ASCII assumptions.

---

## 3. Litmus tests (non-negotiable checkpoints)

If **any** of these fail, you are **not** ready for Skia or Typst.

### Test 1: Renderer swap

**Goal:** Replace the ASCII renderer with a dummy backend.

```python
class DummyRenderer:
    def draw(self, scene):
        pass
```

**Pass:** Scene and animations still run without modification.

**Fail:** Renderer logic leaked into the engine.

---

### Test 2: Headless execution

Run with:

- No terminal output
- No `print` calls anywhere in the engine

**Pass:** The animation still computes correctly.

---

### Test 3: Deterministic replay

Run the same scene twice. **Frame-by-frame output must be identical.**

**Pass:** No time-based randomness, no hidden state.

---

### Test 4: Timeline purity

At time `t`, the result must depend **only** on:

- Scene graph state
- Timeline definitions

**Fail:** If `update()` or manual mutation affects visuals.

---

### Test 5: Animation isolation

Disable one animator, for example:

```python
scene.remove_animation(...)
```

**Pass:** No side effects on other animations.

---

### Test 6: Node purity

Nodes must **not** know about:

- Renderer
- Output format
- Skia or ASCII
- Typst

They only know:

- Position
- Properties
- Children

---

## 4. TODOs before Skia / Typst

This is the actual checklist.

### Phase A — Architecture freeze (critical)

**TODO A1: Eliminate dual motion systems**

- [ ] Remove any `update()`-based motion (keep only logic if needed)
- [ ] Ensure all motion = Timeline + Animator

**TODO A2: Enforce property ownership**

- [ ] Node owns **only** data (`x`, `y`, `r`, etc.)
- [ ] No animation logic inside `Node` subclasses

**TODO A3: Remove “progress hacks”**

- [ ] `Circle.progress` must only be controlled by `CircleOutline`
- [ ] No manual external writes

**TODO A4: Make timeline authoritative**

- [ ] `apply_timeline(scene, t)` is **only** mutation entry point

### Phase B — Animation system cleanup

**TODO B1: Standardize Animator API**

- [ ] All animators implement:

```python
apply(node, t: float)
```

**TODO B2: Add compositors**

- [ ] `Sequence`
- [ ] `Parallel`
- [ ] `Delay`

**TODO B3: Add easing layer**

- [ ] `smoothstep` default
- [ ] Optional easing injection

**TODO B4: Remove “special-case animators”**

- [ ] No geometry-specific hacks in renderer
- [ ] `CircleOutline` must be generic property animation

### Phase C — Scene graph stabilization

**TODO C1: Tree purity**

- [ ] Node children only define structure
- [ ] No animation state in tree

**TODO C2: Transform rules**

- [ ] Parent → child transforms are deterministic
- [ ] No renderer-dependent offsets

**TODO C3: Coordinate system lock**

- [ ] Fix one coordinate system (grid or float → grid mapping)
- [ ] Do **not** mix

### Phase D — System verification

**TODO D1: Headless runner**

- [ ] CLI mode that runs scenes without rendering

**TODO D2: Snapshot tests**

- [ ] Frame-by-frame output comparison

**TODO D3: Timeline debug mode**

- [ ] Print active animations per frame

---

## 5. Only after all of that → Skia

At that point you can **safely** introduce Skia.

**Skia becomes:**

- Renderer backend only
- No knowledge of timeline
- No animation logic

**Intended replacement:**

```text
ASCII canvas → Skia canvas
```

**Not:**

```text
engine rewrite → Skia integration
```

---

## 6. Only after Skia → Typst

Then integrate **Typst**, but only as:

- Text → vector shapes, or
- Layout → precomputed nodes

**Not** inside the animation system.

---

## 7. Final mental model (three layers)

You are building three layers:

### 1. Engine (yours)

- Timeline
- Scene graph
- Animation system

### 2. Renderer (Skia later)

- Turns geometry into pixels

### 3. Content compiler (Typst later)

- Turns text into geometry

---

## 8. If you follow the wrong order

You get:

- Skia leakage into core
- Typst dictating layout rules
- Renderer-dependent animation bugs

---

## TL;DR

Before Skia and Typst, you must achieve:

- **Single** animation system (timeline only)
- **Pure** scene graph (no logic leakage)
- **Deterministic** replay
- **Renderer** independence
- **Composable** animators
- **Stable** coordinate system

---

## Next step (optional)

If you want a concrete picture of the end state, ask for a **golden architecture diagram** of the engine *before* Skia integration — that is often the point where projects either lock the design in or need a full refactor.
