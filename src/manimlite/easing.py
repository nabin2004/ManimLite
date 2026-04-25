"""Easing curves for animations (implementation pending)."""

from __future__ import annotations


def linear(t: float) -> float:
    """Identity easing."""
    return t


def ease_in_out_quad(t: float) -> float:
    """Quadratic ease-in-out on [0, 1]."""
    if t < 0.5:
        return 2.0 * t * t
    return 1.0 - ((-2.0 * t + 2.0) ** 2) / 2.0


def cubic_bezier(t: float, p1x: float, p1y: float, p2x: float, p2y: float) -> float:
    """Evaluate Y at ``t`` for a cubic Bézier from (0,0) to (1,1) with control points.

    Stub: returns ``t`` (real implementation will sample the Bézier curve).
    """
    _ = p1x, p1y, p2x, p2y
    return t
