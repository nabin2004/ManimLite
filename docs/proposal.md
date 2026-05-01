# ManimLite — Project Proposal

**Unofficial Lightweight Animation Engine**  
Inspired by ManimCE | Built for Speed & LLM Codegen

**Author:** Nabin Oli  
**Version:** 0.1 Alpha Proposal  
**Date:** April 2025  
**License:** MIT (proposed)  
**Status:** Pre-development

---

## Executive Summary

ManimLite is a proposed lightweight Python animation engine designed as an alternative to ManimCE for educational content creation.

It focuses on:

- ~10× faster cold rendering
- ~80 MB install size (vs ~3 GB ManimCE)
- LLM-friendly API design for reliable code generation

**Core idea:** The rendering stack is the bottleneck, not animation logic.

By replacing heavy dependencies (LaTeX, Cairo, disk-based rendering pipeline), ManimLite aims to deliver equivalent educational animation quality with drastically lower overhead.

**Voice-over:** Local narration via **Kitten TTS** (optional dependency, Apache-2.0), mixed into the output timeline without a cloud API.

---

## 1. Motivation & Problem Statement

### 1.1 Why Manim is Heavy

ManimCE includes:

- LaTeX / TeX Live → 2–4 GB
- Cairo / Pango → ~180 MB
- FFmpeg subprocess pipeline
- SciPy / NumPy overhead
- OpenGL stack (unused for most 2D content)

Most of this is not required for basic educational animations.

### 1.2 Real Bottleneck

In practice:

- <5% runtime = animation logic
- \>95% runtime =:
  - LaTeX cold starts
  - disk writes (frame pipeline)
  - FFmpeg encoding

A 10-second scene often takes 60–90 seconds to render.

### 1.3 LLM Codegen Issue

ManimCE API is:

- Deep inheritance-based
- Verbose
- Easy to misuse

Result:

- High error rate in AI-generated code
- Debug-heavy workflow
- Poor first-pass success rate

ManimLite fixes this with a flat, typed API.

---

## 2. Competitor Analysis

| Library       | Language | Install | Cold Start | Math           | LLM-Friendly | Use Case          |
| ------------- | -------- | ------- | ---------- | -------------- | ------------ | ----------------- |
| ManimCE       | Python   | ~3 GB   | 30–90s     | Full LaTeX     | Low          | General animation |
| ManimLite     | Python   | ~80 MB  | 2–5s       | Typst/SVG      | High         | Edu animations    |
| Remotion      | JS       | ~500 MB | 3–8s       | MathJax        | Medium       | React video       |
| Motion Canvas | TS       | ~400 MB | 2–4s       | KaTeX          | Medium       | CS videos         |
| D3.js         | JS       | ~2 MB   | \<1s        | None           | High         | Data viz          |
| matplotlib    | Python   | ~60 MB  | 3–6s       | Optional LaTeX | Medium       | Scientific plots  |
| Blender       | Python   | ~3 GB   | 10–30s     | None           | Low          | 3D rendering      |

### Key Positioning

ManimLite is:

- Python-native
- Lightweight (\<100 MB core)
- No LaTeX dependency
- Designed for LLM code generation
- Optional **local** Kitten TTS for teaching voice-overs (no Marp/slide stack in v0.1 scope)

---

## 3. Technical Architecture

### 3.1 Replacement Stack

- LaTeX → Typst (Rust-based, fast SVG output)
- Cairo → Skia-Python (Chrome rendering engine)
- FFmpeg subprocess → PyAV (libav in-memory)
- Class hierarchy → flat dataclass system

### 3.2 Core Design

#### Scene Graph

- Node-based structure
- Every object implements `draw(canvas)` protocol

#### Timeline System

- Time-based animation tuples: `(start, end, node, animator)`

#### Math Rendering

- Typst cached per expression
- SVG reused via hash cache

#### Video Encoding

- Frames streamed directly into H.264 via PyAV
- No disk-based frame storage

#### Voice-over (teaching)

- **Kitten TTS** neural TTS (local, ONNX, Hugging Face Hub models)
- pydub for mixing narration with optional background music
- Muxed with video in PyAV

### 3.3 Package Structure

- `core.py` → engine + timeline
- `shapes.py` → primitives
- `text.py` → text + math + code
- `animate.py` → animation system
- `easing.py` → motion curves
- `render.py` → renderer
- `export.py` → output formats
- `audio/` → mixer + voice-over adapters

---

## 4. Tech Stack

| Concern    | Choice        |
| ---------- | ------------- |
| Rendering  | Skia-Python   |
| Math       | Typst → SVG   |
| Encoding   | PyAV          |
| Audio mix  | pydub         |
| Voice TTS  | Kitten TTS (local) |
| Numerics   | NumPy         |
| Code style | Pygments      |
| Tests      | pytest        |
| Packaging  | uv + hatchling|
| Distribution (later) | Docker |

---

## 5. TODO Breakdown

### Phase 0 — Setup

- Repo scaffold
- Node + Timeline core
- CI pipeline
- Type system setup

### Phase 1 — Renderer

- Skia integration
- Frame pipeline
- PyAV encoding
- Basic animations

### Phase 2 — Primitives

- Shapes (circle, line, polygon)
- Text rendering
- MathExpr via Typst
- CodeBlock rendering

### Phase 3 — Animation System

- Fade, move, transform
- Easing functions
- Group animations

### Phase 4 — Audio

- Audio track support
- Kitten TTS voice-over + pydub mixing

### Phase 5 — Templates

- Intro/outro scenes
- Colour themes

### Phase 6 — Packaging

- Docker image
- PyPI release

### Phase 7 — Docs

- MkDocs site
- Examples gallery
- Migration guide

---

## 6. Roadmap (summary)

See [roadmap.md](roadmap.md) for version milestones.

---

## 7. Limitations

- No 3D support
- No physics simulation
- No live preview
- No full LaTeX compatibility
- Linux/macOS first release

---

## 8. Out of scope (v0.1)

- Marp or slide-deck integration (deferred; focus on MP4 + narration)
- Cloud TTS (optional future backends behind the same protocol)
