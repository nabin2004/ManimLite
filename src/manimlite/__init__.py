"""ManimLite — lightweight educational animation engine (pre-alpha stubs)."""

from __future__ import annotations

__version__ = "0.1.0a0"

from manimlite.audio import KittenVoiceOverBackend, VoiceOver
from manimlite.core import Node, Scene, Timeline
from manimlite.renderer import Renderer
from manimlite.text import CodeBlock, MathExpr, Text

__all__ = [
    "CodeBlock",
    "KittenVoiceOverBackend",
    "MathExpr",
    "Node",
    "Renderer",
    "Scene",
    "Text",
    "Timeline",
    "VoiceOver",
    "__version__",
]
