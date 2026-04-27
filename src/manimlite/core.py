"""Scene graph, timeline, and core composition types (implementation pending)."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Drawable(Protocol):
    """Anything that can be drawn onto a canvas; positions accumulate from parents."""

    def draw(self, canvas: Any, ox: float = 0.0, oy: float = 0.0) -> None:
        """Render this node to the given canvas at origin (ox, oy) plus local offset."""
        ...


@dataclass(slots=True)
class Node:
    """Base graph node; subclasses add geometry, style, and children."""

    x: float = 0.0
    y: float = 0.0
    children: list[Node] = field(default_factory=list)

    def add(self, node: Node) -> None:
        self.children.append(node)

    def draw(self, canvas: Any, ox: float = 0.0, oy: float = 0.0) -> None:
        """Propagate origin so child positions are relative to this node."""
        px = ox + self.x
        py = oy + self.y
        for child in self.children:
            child.draw(canvas, px, py)

    def update(self, t: float, dt: float) -> None:
        """Advance simulation time; subclasses override and call Node.update for children."""
        for child in self.children:
            child.update(t, dt)


@dataclass(slots=True)
class Circle(Node):
    """Discrete circle outline in grid space; children draw in parent's frame."""

    r: float = 1.0
    ch: str = "#"

    def draw(self, canvas: Any, ox: float = 0.0, oy: float = 0.0) -> None:
        cx = ox + self.x
        cy = oy + self.y
        n = max(8, int(self.r * 8))
        for i in range(n):
            t = 2 * math.pi * i / n
            px = int(round(cx + self.r * math.cos(t)))
            py = int(round(cy + self.r * math.sin(t)))
            canvas.set_pixel(px, py, self.ch)
        Node.draw(self, canvas, cx, cy)


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

    def add_node(self, node: Node) -> None:
        """Add a node to the scene graph """
        self.root.add(node)

    def add_animation(self, start: float, end: float, target: Node, animator: Any) -> None:
        """Add an animation to the timeline."""
        self.timeline = self.timeline.add(float(start), float(end), target, animator)