"""Smoke-check Skia, Typst, math cache, text/code rendering, and optional MP4 export.

Run from the repo root::

    python examples/check_skia_typst.py
    python examples/check_skia_typst.py --mp4   # also writes a tiny ./check_skia_typst.mp4

Exit codes:

- ``0`` — all required checks passed (Typst optional: warnings only if CLI missing).
- ``1`` — at least one check failed.

Requires: project installed in the active environment (``uv pip install -e ".[dev]"``).
For math: put ``typst`` on ``PATH`` (see ``docs/guides/setup.md``).
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import numpy as np


def _ok(msg: str) -> None:
    print(f"  [OK]   {msg}")


def _warn(msg: str) -> None:
    print(f"  [WARN] {msg}")


def _fail(msg: str) -> bool:
    print(f"  [FAIL] {msg}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify ManimLite Skia + Typst pipeline.")
    parser.add_argument(
        "--mp4",
        action="store_true",
        help="Encode one short clip to ./check_skia_typst.mp4 (PyAV smoke test).",
    )
    args = parser.parse_args()

    failed = False
    print("ManimLite pipeline check\n")

    # 1) skia-python
    print("1. skia-python")
    try:
        import skia  # noqa: F401

        _ok("import skia")
    except Exception as exc:  # pragma: no cover - example script
        failed |= _fail(f"import skia: {exc}")
        print("\nInstall: uv pip install skia-python")
        return 1

    try:
        surface = skia.Surface(32, 32)
        c = surface.getCanvas()
        c.clear(skia.ColorBLACK)
        f = skia.Font(skia.Typeface("sans-serif"), 12)
        p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
        c.drawString("x", 4, 16, f, p)
        arr = np.asarray(surface.makeImageSnapshot())
        if arr[..., :3].sum() <= 0:
            failed |= _fail("Skia drawString produced no RGB ink")
        else:
            _ok("Skia drawString + snapshot has ink")
    except Exception as exc:  # pragma: no cover
        failed |= _fail(f"Skia mini draw: {exc}")

    # 2) Typst CLI
    print("\n2. Typst CLI")
    typst = shutil.which("typst")
    if typst is None:
        _warn("typst not on PATH — MathExpr will not render (install Typst, see docs/guides/setup.md)")
    else:
        try:
            import subprocess

            v = subprocess.run(
                ["typst", "--version"],
                capture_output=True,
                text=True,
                check=True,
                timeout=5,
            )
            _ok(f"typst: {v.stdout.strip() or '(no stdout)'}")
        except Exception as exc:  # pragma: no cover
            failed |= _fail(f"typst --version: {exc}")

    # 3) Typst cache + MathExpr on Skia
    print("\n3. ManimLite: typst cache + SkiaRenderer")
    from manimlite.core import Scene
    from manimlite.render import SkiaRenderer
    from manimlite.text import CodeBlock, MathExpr, Text
    from manimlite.typst_cache import cached_typst_svg_path

    if typst is None:
        _warn("Skipping MathExpr / cache checks (no typst)")
    else:
        path = cached_typst_svg_path("alpha + beta")
        if path is None or not path.is_file():
            failed |= _fail("cached_typst_svg_path('alpha + beta') did not return a file")
        else:
            _ok(f"Typst cache SVG: {path.name} ({path.stat().st_size} bytes)")

        scene = Scene(width=240, height=80, fps=30.0)
        scene.add_node(MathExpr(typst_source="sum_(i=1)^n i", x=20, y=20, font_size=28.0))
        frame = SkiaRenderer().render_frame(scene, 0.0)
        ink = int(frame[..., :3].astype("int64").sum())
        if ink < 500:
            failed |= _fail(f"MathExpr frame ink too low ({ink}); Skia SVG or Typst may be broken")
        else:
            _ok(f"MathExpr + SkiaRenderer frame ink = {ink}")

    # 4) Text + CodeBlock
    print("\n4. ManimLite: Text + CodeBlock")
    t_scene = Scene(width=320, height=72, fps=30.0)
    t_scene.add_node(Text(content="Hello", x=12, y=12, font_size=22.0, color="#FFFFFF"))
    t_frame = SkiaRenderer().render_frame(t_scene, 0.0)
    t_ink = int(t_frame[..., :3].astype("int64").sum())
    if t_ink < 100:
        failed |= _fail(f"Text frame ink too low ({t_ink})")
    else:
        _ok(f"Text frame ink = {t_ink}")

    c_scene = Scene(width=400, height=100, fps=30.0)
    c_scene.add_node(
        CodeBlock(
            code="def f():\n    return 42\n",
            language="python",
            x=10,
            y=10,
            font_size=14.0,
        )
    )
    c_frame = SkiaRenderer().render_frame(c_scene, 0.0)
    c_ink = int(c_frame[..., :3].astype("int64").sum())
    if c_ink < 100:
        failed |= _fail(f"CodeBlock frame ink too low ({c_ink})")
    else:
        _ok(f"CodeBlock frame ink = {c_ink}")

    # 5) Optional PyAV
    if args.mp4:
        print("\n5. PyAV encode (short MP4)")
        from manimlite.animate import CircleOutline, MoveX
        from manimlite.core import Circle
        from manimlite.export import PyAVEncoder

        e_scene = Scene(width=320, height=240, fps=10.0, duration=0.4)
        e_scene.add_node(Text(content="MP4", x=40, y=100, font_size=36.0))
        circ = Circle(x=220, y=120, r=40, progress=0.0)
        e_scene.add_node(circ)
        e_scene.add_animation(0.0, 0.4, circ, CircleOutline())
        e_scene.add_animation(0.0, 0.4, circ, MoveX(220.0, 180.0))

        out = Path("check_skia_typst.mp4")
        PyAVEncoder(scene=e_scene, output_path=out).encode(verbose=False)
        if not out.is_file() or out.stat().st_size < 200:
            failed |= _fail(f"MP4 missing or too small: {out}")
        else:
            _ok(f"wrote {out.resolve()} ({out.stat().st_size} bytes)")

    print()
    if failed:
        print("Result: FAILED")
        return 1
    print("Result: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
