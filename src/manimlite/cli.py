"""Command-line interface for ManimLite."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Annotated

import typer

from manimlite.core import Scene

app = typer.Typer(no_args_is_help=True, help="ManimLite — lightweight animation CLI.")


@app.command("backends")
def list_backends() -> None:
    """List named render targets (ASCII terminal vs Skia frame buffer)."""

    typer.echo("ascii — manimlite.Renderer (terminal grid)")
    typer.echo("skia  — manimlite.SkiaRenderer (RGBA ndarray via skia-python)")


def _import_scene_module(scene_file: Path) -> ModuleType:
    """Load ``scene_file`` as a module (``_user_scene``)."""
    spec = importlib.util.spec_from_file_location("_user_scene", str(scene_file))
    if spec is None or spec.loader is None:
        raise typer.BadParameter(f"Cannot load module from {scene_file}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_user_scene"] = mod
    spec.loader.exec_module(mod)
    return mod


def _scene_from_module(mod: ModuleType, scene_file: Path) -> Scene:
    """Return a :class:`~manimlite.core.Scene` from a loaded user module.

    Looks for (in order):

    1. ``build_scene()`` callable
    2. Module-level ``scene``
    """

    if hasattr(mod, "build_scene") and callable(mod.build_scene):
        obj = mod.build_scene()
        if isinstance(obj, Scene):
            return obj
        raise typer.BadParameter("build_scene() did not return a Scene instance")

    if hasattr(mod, "scene") and isinstance(mod.scene, Scene):
        return mod.scene

    raise typer.BadParameter(
        f"No build_scene() function or 'scene' attribute found in {scene_file}"
    )


@app.command()
def render(
    scene_file: Annotated[
        Path,
        typer.Argument(help="Path to scene .py", exists=True, readable=True),
    ],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Output MP4 path (default: <scene_name>.mp4)"),
    ] = None,
    width: Annotated[
        int | None,
        typer.Option(help="Override scene width"),
    ] = None,
    height: Annotated[
        int | None,
        typer.Option(help="Override scene height"),
    ] = None,
    fps: Annotated[
        float | None,
        typer.Option(help="Override scene FPS"),
    ] = None,
    quiet: Annotated[
        bool,
        typer.Option("--quiet", "-q", help="Suppress progress output"),
    ] = False,
) -> None:
    """Render a scene file to MP4 video."""
    from manimlite.export import PyAVEncoder
    from manimlite.render import SkiaRenderer

    mod = _import_scene_module(scene_file)
    scene = _scene_from_module(mod, scene_file)

    if width is not None:
        scene.width = width
    if height is not None:
        scene.height = height
    if fps is not None:
        scene.fps = fps

    if output is None:
        output = Path(scene_file.stem + ".mp4")

    get_renderer = getattr(mod, "get_skia_renderer", None)
    renderer = (
        get_renderer()
        if callable(get_renderer)
        else SkiaRenderer()
    )
    encoder = PyAVEncoder(scene=scene, output_path=output, renderer=renderer)
    result = encoder.encode(verbose=not quiet)
    typer.echo(f"Rendered: {result} ({result.stat().st_size:,} bytes)")


def main() -> None:
    """Entry point for ``python -m manimlite`` style invocation."""
    app()


if __name__ == "__main__":
    main()
