"""Animation helpers, animator protocol, and timeline evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Protocol, runtime_checkable

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
    """Apply all timeline entries at global scene time ``t`` (segment-local ``u`` then optional ``ease``).

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
class CircleOutline:
    """Set ``Circle.progress`` in [0, 1] from segment-local ``t``."""

    def apply(self, node: Node, t: float) -> None:
        if not isinstance(node, Circle):
            raise TypeError("CircleOutline only applies to Circle nodes")
        node.progress = max(0.0, min(1.0, t))


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
