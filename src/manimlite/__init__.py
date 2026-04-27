"""ManimLite — lightweight educational animation engine (pre-alpha stubs)."""

from __future__ import annotations

__version__ = "0.1.0a0"

from manimlite.animate import (
    Animator,
    CircleOutline,
    Delay,
    MoveX,
    Parallel,
    Sequence,
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
    "Delay",
    "KittenVoiceOverBackend",
    "MathExpr",
    "MoveX",
    "Node",
    "Parallel",
    "Renderer",
    "Scene",
    "Sequence",
    "Text",
    "apply_timeline",
    "lerp",
    "smoothstep",
    "Timeline",
    "VoiceOver",
    "__version__",
]
