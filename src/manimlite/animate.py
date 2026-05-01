"""Animation helpers, animator protocol, and timeline evaluation."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

from manimlite.core import Circle, Node, Scene

# (global_t, start, end, target, animator, u_eased) — invoked after ``apply`` succeeds.
TimelineOnApply = Callable[[float, float, float, Node, Any, float], None]


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation from ``a`` to ``b`` with ``t`` in [0, 1]."""
    return a + (b - a) * t


def smoothstep(t: float) -> float:
    """Hermite ease in-out; clamps ``t`` to [0, 1]."""
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def apply_timeline(
    scene: Scene,
    t: float,
    *,
    ease: Callable[[float], float] | None = smoothstep,
    on_apply: TimelineOnApply | None = None,
) -> None:
    """Apply all timeline entries at global scene time ``t``.

    Maps global time to segment-local ``u``, then optionally applies ``ease``.

    If ``on_apply`` is set, it is called after each successful ``anim.apply`` with
    ``(t, start, end, target, anim, u_eased)`` for debugging or tooling.
    """
    for start, end, target, anim in scene.timeline.entries:
        if end <= start:
            continue
        if t <= start:
            u = 0.0
        elif t >= end:
            u = 1.0
        else:
            u = (t - start) / (end - start)
        u_eased = ease(u) if ease is not None else u
        apply_fn = getattr(anim, "apply", None)
        if apply_fn is not None:
            apply_fn(target, u_eased)
            if on_apply is not None:
                on_apply(t, start, end, target, anim, u_eased)


@runtime_checkable
class Animator(Protocol):
    """Interpolates a node between t=0 and t=1 within a timeline segment."""

    def apply(self, node: Node, t: float) -> None:
        """Apply eased progress ``t`` in [0, 1] to ``node``."""
        ...


@dataclass(slots=True)
class MoveX:
    """Set ``node.x`` between ``x0`` (t=0) and ``x1`` (t=1)."""

    x0: float
    x1: float

    def apply(self, node: Node, t: float) -> None:
        node.x = lerp(self.x0, self.x1, t)


@dataclass(slots=True)
class MoveY:
    """Set ``node.y`` between ``y0`` (t=0) and ``y1`` (t=1)."""

    y0: float
    y1: float

    def apply(self, node: Node, t: float) -> None:
        node.y = lerp(self.y0, self.y1, t)


@dataclass(slots=True)
class CircleOutline:
    """Set ``Circle.progress`` in [0, 1] from segment-local ``t``."""

    def apply(self, node: Node, t: float) -> None:
        if not isinstance(node, Circle):
            raise TypeError("CircleOutline only applies to Circle nodes")
        node.progress = max(0.0, min(1.0, t))


class Parallel:
    """Run several animators on the same node with the same segment-local ``t``."""

    __slots__ = ("animators",)

    def __init__(self, *animators: Any) -> None:
        self.animators = animators

    def apply(self, node: Node, t: float) -> None:
        for anim in self.animators:
            apply_fn = getattr(anim, "apply", None)
            if apply_fn is not None:
                apply_fn(node, t)


class Sequence:
    """Partition ``t ∈ [0, 1]`` into equal sub-segments and run exactly one child at a time.

    Only the active sub-animator runs each frame; other properties keep their previous values.
    Align segment boundaries so ``local_t=1`` of segment ``k`` matches
    ``local_t=0`` of ``k+1`` where needed.
    """

    __slots__ = ("animators",)

    def __init__(self, *animators: Any) -> None:
        self.animators = animators

    def apply(self, node: Node, t: float) -> None:
        n = len(self.animators)
        if n == 0:
            return
        t = max(0.0, min(1.0, t))
        segment = 1.0 / n
        i = min(int(t / segment), n - 1)
        local_t = (t - i * segment) / segment if segment > 0 else 0.0
        apply_fn = getattr(self.animators[i], "apply", None)
        if apply_fn is not None:
            apply_fn(node, local_t)


@dataclass(slots=True)
class Delay:
    """Run ``animator`` only when ``start <= t <= end`` (``t`` is parent's segment-local time).

    Outside that window this is a no-op (inner ``apply`` is not called). For a pinned start pose,
    set initial node state or use another animator.
    """

    animator: Any
    start: float
    end: float

    def __post_init__(self) -> None:
        if not (0.0 <= self.start < self.end <= 1.0):
            raise ValueError("Delay requires 0 <= start < end <= 1")

    def apply(self, node: Node, t: float) -> None:
        if t < self.start or t > self.end:
            return
        span = self.end - self.start
        local_t = (t - self.start) / span
        apply_fn = getattr(self.animator, "apply", None)
        if apply_fn is not None:
            apply_fn(node, local_t)


@dataclass(slots=True)
class Animation:
    """Concrete animation wrapper (fade, move, transform — TBD)."""

    name: str = "noop"

    def as_animator(self) -> Any:
        """Return an ``Animator`` implementation (stub)."""
        return _NoopAnimator()


class _NoopAnimator:
    """Placeholder animator."""

    def apply(self, node: Node, t: float) -> None:
        _ = node, t
