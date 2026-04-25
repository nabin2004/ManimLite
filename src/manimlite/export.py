"""Video export via PyAV (implementation pending)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from manimlite.core import Scene


@dataclass(slots=True)
class PyAVEncoder:
    """Encodes a rendered scene to H.264 MP4 without intermediate frame files."""

    scene: Scene
    output_path: Path

    def encode(self, frame_source: Any) -> None:
        """Stream frames from ``frame_source`` into ``output_path`` (stub)."""
        _ = frame_source
