"""Command-line interface for MotionGram."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Annotated

import typer

from motiongram.core import Scene

app = typer.Typer(
    no_args_is_help=True,
    help="MotionGram 📽️ — The grammar of motion graphics.",
)


@app.command("backends")
def list_backends() -> None:
    """List named render targets (ASCII terminal vs Skia frame buffer)."""

    typer.echo("ascii — motiongram.Renderer (terminal grid)")
    typer.echo("skia  — motiongram.SkiaRenderer (RGBA ndarray via skia-python)")


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
    """Return a :class:`~motiongram.core.Scene` from a loaded user module.

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
        typer.Argument(help="Path to scene .py or .yaml", exists=True, readable=True),
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
    frames_dir: Annotated[
        Path | None,
        typer.Option(
            "--frames-dir",
            help="Write each frame as PNG under this directory (same pass as MP4)",
        ),
    ] = None,
    quiet: Annotated[
        bool,
        typer.Option("--quiet", "-q", help="Suppress progress output"),
    ] = False,
) -> None:
    """Render a scene file to MP4 video."""
    from motiongram.export import PyAVEncoder
    from motiongram.render import SkiaRenderer

    linear_timeline = False
    suffix = scene_file.suffix.lower()
    if suffix in (".yaml", ".yml"):
        from motiongram.manifest.loader import render_manifest

        program, scene = render_manifest(scene_file)
        if output is None:
            output = program.output_path
        renderer = SkiaRenderer(clear_color=program.clear_color)
        linear_timeline = program.uses_custom_easing
        if program.voiceover_paths and not quiet:
            typer.echo(
                "Note: voiceover paths detected but audio mux is not yet supported.",
                err=True,
            )
    else:
        mod = _import_scene_module(scene_file)
        scene = _scene_from_module(mod, scene_file)
        if output is None:
            output = Path(scene_file.stem + ".mp4")
        get_renderer = getattr(mod, "get_skia_renderer", None)
        renderer = (
            get_renderer()
            if callable(get_renderer)
            else SkiaRenderer()
        )

    if width is not None:
        scene.width = width
    if height is not None:
        scene.height = height
    if fps is not None:
        scene.fps = fps

    encoder = PyAVEncoder(
        scene=scene,
        output_path=output,
        renderer=renderer,
        frames_dir=frames_dir,
        linear_timeline=linear_timeline,
    )
    result = encoder.encode(verbose=not quiet)
    msg = f"Rendered: {result} ({result.stat().st_size:,} bytes)"
    if frames_dir is not None:
        msg += f"; frames: {frames_dir.expanduser().resolve()}"
    typer.echo(msg)



@app.command()
def preview(
    scene_file: Annotated[
        Path,
        typer.Argument(help="Path to YAML manifest", exists=True, readable=True),
    ],
    port: Annotated[
        int,
        typer.Option("--port", help="HTTP port for preview server"),
    ] = 8765,
    host: Annotated[
        str,
        typer.Option("--host", help="Bind address"),
    ] = "127.0.0.1",
    time: Annotated[
        str,
        typer.Option("--time", help="Initial scrub time (e.g. 0s, 2.5)"),
    ] = "0s",
    video_on_save: Annotated[
        bool,
        typer.Option(
            "--video-on-save",
            help="Background full MP4 encode after saves (debounced)",
        ),
    ] = False,
) -> None:
    """Live-preview a YAML manifest in the browser (reloads on save)."""
    suffix = scene_file.suffix.lower()
    if suffix not in (".yaml", ".yml"):
        raise typer.BadParameter("preview only supports .yaml / .yml manifests")

    from motiongram.preview import run_preview_server

    run_preview_server(
        scene_file,
        host=host,
        port=port,
        video_on_save=video_on_save,
        initial_time=time,
    )



def main() -> None:
    """Entry point for ``python -m motiongram`` style invocation."""
    app()


if __name__ == "__main__":
    main()
