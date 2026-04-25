"""Animation descriptors and animator protocol (implementation pending)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

from manimlite.core import Node


@runtime_checkable
class Animator(Protocol):
    """Interpolates a node between t=0 and t=1 within a timeline segment."""

    def apply(self, node: Node, t: float) -> None:
        """Apply eased progress ``t`` in [0, 1] to ``node``."""
        ...


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

