"""ManimLite — lightweight educational animation engine (pre-alpha stubs)."""

from __future__ import annotations

__version__ = "0.1.0a0"

from manimlite.animate import (
    Animator,
    CircleOutline,
    Delay,
    MoveX,
    MoveY,
    Parallel,
    Sequence,
    apply_timeline,
    lerp,
    smoothstep,
)
from manimlite.audio import KittenVoiceOverBackend, VoiceOver
from manimlite.canvas import Canvas, NullCanvas, RecordingCanvas
from manimlite.core import Circle, Node, Scene, Timeline
from manimlite.engine import step_frame
from manimlite.render import SkiaCanvas, SkiaRenderer
from manimlite.renderer import Renderer, ascii_frame_sha256, ascii_frame_text
from manimlite.text import CodeBlock, MathExpr, Text
from manimlite.export import PyAVEncoder
from manimlite.typst_cache import cached_typst_svg_path, typst_cache_key

__all__ = [
    "Animator",
    "Canvas",
    "NullCanvas",
    "RecordingCanvas",
    "Circle",
    "CircleOutline",
    "CodeBlock",
    "Delay",
    "KittenVoiceOverBackend",
    "MathExpr",
    "MoveX",
    "MoveY",
    "Node",
    "Parallel",
    "PyAVEncoder",
    "Renderer",
    "Scene",
    "Sequence",
    "SkiaCanvas",
    "SkiaRenderer",
    "Text",
    "apply_timeline",
    "ascii_frame_sha256",
    "ascii_frame_text",
    "cached_typst_svg_path",
    "step_frame",
    "lerp",
    "smoothstep",
    "Timeline",
    "typst_cache_key",
    "VoiceOver",
    "__version__",
]
