# Use cases

Primary actors: **Educator**, **Developer**, **LLM Agent**, **CI Pipeline**.

---

## UC-1 — Render a short concept clip

**Actor:** Educator  
**Goal:** Export a 30–120 s MP4 explaining one idea.  
**Preconditions:** ManimLite installed; scene file written.  
**Main flow:**

1. Author defines `Scene`, shapes, and timeline.
2. Run `manimlite render scene.py`.
3. System renders frames and encodes MP4.
4. User uploads MP4 to LMS or YouTube.

**Postconditions:** MP4 exists at configured path.  
**Extensions:** Add `VoiceOver` segments (UC-5).

---

## UC-2 — Math equation without LaTeX install

**Actor:** Educator / Developer  
**Goal:** Display a typeset equation.  
**Flow:** Use `MathExpr(typst_source="...")`; engine calls Typst → SVG → Skia; cache reused on repeated expressions.

**Failure:** Typst missing or source error → actionable error with line context.

---

## UC-3 — LLM-generated scene first pass

**Actor:** LLM Agent (supervised by human)  
**Goal:** Emit valid Python using only documented public symbols.  
**Flow:** Agent reads `AGENTS.md` + `api-spec.md`; outputs dataclass-based scene; user runs render.

**Success measure:** High share of scenes that import and render without edit (NFR-3).

---

## UC-4 — Batch render in CI

**Actor:** CI Pipeline  
**Goal:** Verify scenes still build after library upgrade.  
**Flow:** Headless Linux runner; `uv sync`; `pytest` + optional golden-frame checks.

---

## UC-5 — Local narration for teaching

**Actor:** Educator  
**Goal:** Add voice-over without cloud API keys.  
**Flow:**

1. Install optional `tts` extra (Kitten TTS wheel + `soundfile`).
2. Declare `VoiceOver(text=..., voice="Jasper", start=...)` and synthesize with `KittenVoiceOverBackend()`.
3. Scene muxes synthesized audio with video.

**Alternatives:** Pre-baked WAV files (future FR extension) via same mixer path.

---

## UC-6 — Code walkthrough with highlighting

**Actor:** Developer / Educator  
**Goal:** Show highlighted source in the video.  
**Flow:** `CodeBlock(code=..., language="python")` rendered via Pygments styles → Skia.

---

## UC-7 — Contributor adds a new shape

**Actor:** Contributor  
**Goal:** Extend primitives safely.  
**Flow:** Subclass or compose `Node`, implement `draw`, add tests, update SRS traceability.

---

## UC-8 — Theme / template intro (future)

**Actor:** Content creator  
**Goal:** Reuse branded intro.  
**Flow (v0.4+):** Load template package; parameters for colors/logo.
