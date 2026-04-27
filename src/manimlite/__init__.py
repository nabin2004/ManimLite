"""ManimLite — lightweight educational animation engine (pre-alpha stubs)."""

from __future__ import annotations

__version__ = "0.1.0a0"

from manimlite.animate import (
    Animator,
    CircleOutline,
    MoveX,
    apply_timeline,
    lerp,
    smoothstep,
)
from manimlite.audio import KittenVoiceOverBackend, VoiceOver
from manimlite.core import Circle, Node, Scene, Timeline
from manimlite.renderer import Renderer
from manimlite.text import CodeBlock, MathExpr, Text

__all__ = [
    "Animator",
    "Circle",
    "CircleOutline",
    "CodeBlock",
    "KittenVoiceOverBackend",
    "MathExpr",
    "MoveX",
    "Node",
    "Renderer",
    "Scene",
    "Text",
    "apply_timeline",
    "lerp",
    "smoothstep",
    "Timeline",
    "VoiceOver",
    "__version__",
]
