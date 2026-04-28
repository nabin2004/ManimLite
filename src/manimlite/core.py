"""Scene graph, timeline, and core composition types (implementation pending)."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from manimlite.canvas import Canvas


@runtime_checkable
class Drawable(Protocol):
    """Anything that can be drawn onto a canvas; positions accumulate from parents."""

    def draw(self, canvas: Canvas, ox: float = 0.0, oy: float = 0.0) -> None:
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

    def draw(self, canvas: Canvas, ox: float = 0.0, oy: float = 0.0) -> None:
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
    """Circle outline (raster) plus optional vector style fields (used by Skia backends)."""

    r: float = 1.0
    ch: str = "#"
    progress: float = 1.0  # 1 = full outline; animate via timeline (e.g. CircleOutline).

    fill_color: str = "#FFFFFF"
    stroke_color: str | None = None
    stroke_width: float = 0.0

    @property
    def radius(self) -> float:
        """Alias for ``r`` (compat with older ``shapes.Circle(radius=…)`` examples)."""
        return self.r

    @radius.setter
    def radius(self, value: float) -> None:
        self.r = float(value)

    def draw(self, canvas: Canvas, ox: float = 0.0, oy: float = 0.0) -> None:
        cx = ox + self.x
        cy = oy + self.y
        n = max(8, int(self.r * 8))
        p = max(0.0, min(1.0, self.progress))
        k = int(n * p)
        for i in range(k):
            ang = 2 * math.pi * i / n
            px = int(round(cx + self.r * math.cos(ang)))
            py = int(round(cy + self.r * math.sin(ang)))
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

    def without_entry(self, index: int) -> Timeline:
        """Return a new timeline with the entry at ``index`` removed (other entries keep order)."""
        n = len(self.entries)
        if not (0 <= index < n):
            raise IndexError(f"timeline entry index out of range: {index} (len={n})")
        return Timeline(
            entries=tuple(self.entries[i] for i in range(n) if i != index),
        )


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

    def remove_animation_at(self, index: int) -> None:
        """Remove one timeline entry by index (see :meth:`Timeline.without_entry`)."""
        self.timeline = self.timeline.without_entry(index)