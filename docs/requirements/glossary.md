# Glossary

| Term | Definition |
| ---- | ---------- |
| **Animator** | Object that applies eased progress in `[0, 1]` to a `Node` over a timeline segment. |
| **Cold render** | First render of a scene in a fresh process, including dependency and cache warm-up relevant to that run. |
| **ManimCE** | Manim Community Edition, the reference ecosystem Typmotion is inspired by (not affiliated). |
| **Node** | Element of the scene graph; may have children and local drawing behavior. |
| **Kitten TTS** | Lightweight local neural TTS (ONNX, Apache-2.0). Default implementation is `KittenVoiceOverBackend` when the `tts` extra is installed. |
| **PyAV** | Python bindings to **libav**/**FFmpeg** libraries for in-process demux/mux/encode. |
| **Scene** | Root object: dimensions, frame rate, duration, root `Node`, and `Timeline`. |
| **Skia** | 2D graphics engine used by Chromium; exposed to Python via **skia-python**. |
| **Timeline** | Ordered collection of `(start, end, target, animator)` tuples. |
| **Typst** | Modern typesetting system used to produce SVG for math without LaTeX. |
| **Voice-over** | Narration track synthesized or supplied as audio, aligned to scene time. |
