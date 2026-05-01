"""Compile Typst math to cached SVG on disk (Typst stays out of the animation layer)."""

from __future__ import annotations

import contextlib
import hashlib
import os
import shutil
import subprocess
from pathlib import Path


def _cache_root() -> Path:
    base = os.environ.get("MANIMLITE_CACHE_HOME", "")
    if base:
        return Path(base).expanduser() / "typst"
    return Path.home() / ".cache" / "typmotion" / "typst"


def _typst_stub(source: str) -> str:
    s = source.strip()
    if s.startswith("#set") or s.startswith("#page"):
        return s
    return f"""#set page(width: auto, height: auto, margin: 2pt)
#set text(14pt)
$
{s}
$
"""


def typst_cache_key(source: str, *, engine_marker: str = "typmotion_typst_v1") -> str:
    h = hashlib.sha256()
    h.update(engine_marker.encode())
    h.update(b"\n")
    h.update(source.encode())
    return h.hexdigest()


def cached_typst_svg_path(source: str, *, engine_marker: str = "typmotion_typst_v1") -> Path | None:
    """Return path to ``.svg`` compiled from ``source``, or ``None`` if ``typst`` is unavailable.

    Cached by :func:`typst_cache_key`. Idempotent: same source returns the same file.
    """
    if shutil.which("typst") is None:
        return None

    key = typst_cache_key(source, engine_marker=engine_marker)
    root = _cache_root()
    root.mkdir(parents=True, exist_ok=True)
    typ_path = root / f"{key}.typ"
    svg_path = root / f"{key}.svg"

    if svg_path.is_file():
        return svg_path

    typ_path.write_text(_typst_stub(source), encoding="utf-8")
    try:
        subprocess.run(
            ["typst", "compile", str(typ_path), str(svg_path)],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        for p in (svg_path, typ_path):
            with contextlib.suppress(OSError):
                p.unlink(missing_ok=True)
        return None

    return svg_path if svg_path.is_file() else None
