"""Skia-backed frame rendering (implementation pending)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from manimlite.core import Scene


@dataclass(slots=True)
class SkiaRenderer:
    """Renders a ``Scene`` to RGB(A) frame buffers via skia-python."""

    scene: Scene

    def render_frame(self, time: float) -> Any:
        """Return a frame buffer (numpy array or skia surface) for ``time`` (stub)."""
        _ = time
        return None
