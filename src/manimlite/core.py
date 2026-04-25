"""Scene graph, timeline, and core composition types (implementation pending)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Drawable(Protocol):
    """Anything that can be drawn onto a Skia-backed canvas."""

    def draw(self, canvas: Any) -> None:
        """Render this node to the given canvas."""
        ...


@dataclass(slots=True)
class Node:
    """Base graph node; subclasses add geometry, style, and children."""

    children: tuple[Node, ...] = field(default_factory=tuple)

    def draw(self, canvas: Any) -> None:
        """Draw this node and its children (stub)."""
        for child in self.children:
            child.draw(canvas)


@dataclass(slots=True)
class Timeline:
    """Ordered animation tuples: (start, end, target, animator)."""

    entries: tuple[tuple[float, float, Node, Any], ...] = field(default_factory=tuple)

    def add(
        self,
        start: float,
        end: float,
        target: Node,
        animator: Any,
    ) -> Timeline:
        """Return a new timeline with one entry appended (immutable-style API)."""
        return Timeline(entries=(*self.entries, (start, end, target, animator)))


@dataclass(slots=True)
class Scene:
    """Root container: resolution, timing, graph, and timeline."""

    width: int = 1920
    height: int = 1080
    fps: float = 30.0
    duration: float = 5.0
    root: Node = field(default_factory=Node)
    timeline: Timeline = field(default_factory=Timeline)

    def narrate(self, voice_over: Any) -> None:
        """Register narration for mixing into the output audio (stub)."""
        _ = voice_over
