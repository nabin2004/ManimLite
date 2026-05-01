# Software Requirements Specification (SRS)

**Project:** Typmotion  
**Document:** SRS  
**Style:** IEEE 830–style (adapted)  
**Version:** 0.1  
**Status:** Draft  

---

## 1. Introduction

### 1.1 Purpose

This document specifies the functional and non-functional requirements for **Typmotion**, a lightweight Python animation engine for educational video, optimized for small install size, fast cold rendering, and LLM-generated scene code.

### 1.2 Scope

Typmotion shall provide:

- A **scene graph** of drawable nodes
- A **timeline** of animations over wall-clock time
- **2D rendering** to raster frames
- **H.264 MP4** export without writing per-frame image files to disk
- **Math** rendering via Typst to SVG (no TeX Live)
- **Optional local voice-over** via Kitten TTS and pydub mixing

Out of scope for v1.0 unless explicitly added later: 3D, physics simulation, live preview, full LaTeX compatibility, Marp/slide integration, cloud-only TTS.

### 1.3 Definitions, acronyms, abbreviations

See [glossary.md](glossary.md).

### 1.4 References

- Project proposal: [../proposal.md](../proposal.md)
- Software design: [../design/SDD.md](../design/SDD.md)
- ADRs: [../design/adr/](../design/adr/)

### 1.5 Overview

Section 2 describes the product at a high level. Section 3 lists specific requirements. Section 4 covers verification. Appendix A contains a traceability matrix stub.

---

## 2. Overall description

### 2.1 Product perspective

Typmotion is a standalone library and CLI. It is positioned as an alternative to ManimCE for **2D educational** animations where install size and cold start matter. It does not embed a slide framework; output is primarily **MP4** (optional WAV sidecar if needed).

### 2.2 Product functions

1. **Authoring:** Users define scenes in Python using flat, typed constructs.
2. **Composition:** Nodes form a tree; each node can draw itself.
3. **Animation:** Timeline entries map time intervals to animators affecting nodes.
4. **Rendering:** Frames are rasterized with Skia.
5. **Math:** Expressions are compiled with Typst to SVG, cached by content hash.
6. **Export:** Video is encoded with PyAV; audio is muxed when present.
7. **Voice-over:** Optional Kitten TTS synthesis produces narration aligned to the timeline.

### 2.3 User classes and characteristics

| Class            | Needs |
| ---------------- | ----- |
| Educators        | Simple API, fast iteration, MP4 for LMS/YouTube |
| Content creators | Deterministic output, themeability (later) |
| LLM agents       | Small API surface, dataclasses, explicit parameters |
| Contributors     | Clear module boundaries, CI, typed stubs |

### 2.4 Operating environment

- **Language:** Python 3.11+
- **OS (initial):** Linux first; macOS second; Windows best-effort later
- **Hardware:** CPU; optional GPU for Kitten TTS where supported by upstream (`backend="cuda"`)

### 2.5 Design and implementation constraints

- **C-1:** No dependency on system TeX Live or LaTeX for core math path.
- **C-2:** No mandatory subprocess-per-frame **ffmpeg** encoding; use PyAV in-process.
- **C-3:** Core install footprint target ≤ **100 MB** on disk (wheels + minimal assets); voice models are optional downloads.
- **C-4:** Project license **MIT**; optional **Kitten TTS** stack is **Apache-2.0** (per upstream) but large / network-bound — keep behind the `[tts]` extra and document HF model downloads (see ADR-0004).

### 2.6 Assumptions and dependencies

- **Skia-python** wheels available for target platforms.
- **Typst** compiler available at runtime (bundled binary or user-provided path); exact distribution TBD in implementation.
- **libav** available to PyAV (wheel includes bindings).
- **Kitten TTS** ONNX weights may be downloaded from Hugging Face Hub on first use (cache directory per upstream / HF conventions).

---

## 3. Specific requirements

### 3.1 Functional requirements

| ID   | Requirement |
| ---- | ------------- |
| FR-1 | The system shall represent scenes as a **scene graph** of `Node` objects. |
| FR-2 | Each drawable node shall implement a **`draw(canvas)`** protocol invoked by the renderer. |
| FR-3 | The system shall maintain a **timeline** of entries `(start_time, end_time, target_node, animator)`. |
| FR-4 | Frame rasterization at time `t` shall be **deterministic** given fixed scene inputs, resolution, fps, and random seed (if any stochastic effect exists). |
| FR-5 | The system shall export **H.264 MP4** via **PyAV** without requiring an intermediate on-disk PNG/JPEG sequence for normal operation. |
| FR-6 | The system shall render **math** by compiling **Typst** source to **SVG**, with a **content-hash cache** to reuse prior results. |
| FR-7 | The system shall provide primitives: **Circle**, **Line**, **Polygon** with fill/stroke parameters. |
| FR-8 | The system shall support **plain text** labels with font size and color. |
| FR-9 | The system shall support **syntax-highlighted code** via Pygments. |
| FR-10 | The system shall provide **animation descriptors** and an **Animator** protocol applying eased progress in `[0, 1]` to a target node. |
| FR-11 | The system shall provide **easing functions** (at minimum linear and a smooth ease-in-out). |
| FR-12 | The system shall expose a **CLI**: `typmotion render <scene.py>` producing a video file path. |
| FR-13 | The system shall support **optional voice-over**: given text, voice id, and start time, synthesize audio via **Kitten TTS** (default local backend) and place it on the master audio timeline. |
| FR-14 | The system shall **mix** narration and optional background audio with **pydub** before muxing. |
| FR-15 | The system shall define a **`VoiceOverBackend`** protocol to allow alternate backends without breaking the public narration API. |

### 3.2 Non-functional requirements

| ID    | Requirement |
| ----- | ------------- |
| NFR-1 | **Cold render latency:** for a reference 10 s scene (defined in test fixtures), median wall time ≤ **5 s** on a “commodity laptop” profile (to be benchmarked in CI nightly or manual job). |
| NFR-2 | **Install size:** core dependency set (excluding optional Kitten TTS / HF models) shall target ≤ **100 MB** on disk after `pip/uv install`. |
| NFR-3 | **LLM ergonomics:** public API shall prefer **dataclasses**, explicit **constructors**, and **≤20** top-level symbols re-exported from `typmotion` (subject to revision with ADR). |
| NFR-4 | **Reproducibility:** releases shall ship with a **lockfile** (`uv.lock`) and pinned optional extras where feasible. |
| NFR-5 | **License compliance:** `LICENSE` MIT; third-party licenses documented; optional TTS stack documented (Apache-2.0 Kitten + transitive deps). |

### 3.3 External interface requirements

- **Python API:** package `typmotion` under `src/`, typed (`py.typed`).
- **CLI:** Typer-based entry point `typmotion`.
- **Inputs:** Python scene module/path; Typst source strings; optional audio files.
- **Outputs:** MP4 file path; optional logs; optional WAV for debugging.

---

## 4. Verification and validation

| Requirement | Verification |
| ----------- | ------------- |
| FR-1–FR-3 | Unit tests on graph/timeline construction; golden structure snapshots. |
| FR-4 | Golden-frame hash tests on fixed `t` samples (once renderer exists). |
| FR-5 | Integration test: short clip encodes; ffprobe probes stream (optional in CI if libav present). |
| FR-6 | Unit tests: cache hit/miss by hash; Typst error surfaces as structured exception. |
| FR-7–FR-9 | Visual regression tests (deferred) or smoke draw tests. |
| FR-10–FR-11 | Unit tests on easing and animator application. |
| FR-12 | CLI integration test invoking Typer runner. |
| FR-13–FR-15 | Integration test with Kitten TTS in CI (optional / slow job) or mocked backend. |
| NFR-1–NFR-2 | Benchmark scripts + documented hardware profile. |
| NFR-3 | API snapshot / symbol count check in CI. |
| NFR-4–NFR-5 | Legal notices in docs; CI audit of dependency licenses (optional). |

---

## Appendix A — Traceability matrix (stub)

| Req ID | Design doc section | ADR | Test case (planned) |
| ------ | ------------------- | --- | --------------------- |
| FR-5   | [rendering-pipeline.md](../design/rendering-pipeline.md) | ADR-0003 | `tests/integration/test_encode_mp4.py` |
| FR-6   | [rendering-pipeline.md](../design/rendering-pipeline.md) | ADR-0002 | `tests/unit/test_typst_cache.py` |
| FR-13  | [voiceover-adapter.md](../design/voiceover-adapter.md) | ADR-0004 | `tests/integration/test_kitten_voiceover.py` |
| FR-1–3 | [data-model.md](../design/data-model.md) | ADR-0005 | `tests/unit/test_timeline.py` |

*(Expand this table as implementation proceeds.)*
