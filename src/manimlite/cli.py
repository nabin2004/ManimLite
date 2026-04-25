"""Command-line interface (implementation pending)."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

app = typer.Typer(no_args_is_help=True, help="ManimLite — lightweight animation CLI.")


@app.command()
def render(
    scene_file: Annotated[
        Path,
        typer.Argument(help="Path to scene .py", exists=True, readable=True),
    ],
) -> None:
    """Render a scene file to video (stub)."""
    typer.echo(f"Render not yet implemented: {scene_file}")


def main() -> None:
    """Entry point for ``python -m manimlite`` style invocation."""
    app()


if __name__ == "__main__":
    main()
