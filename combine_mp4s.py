"""
combine_mp4s.py
---------------
Walk a project directory, collect all .mp4 files (sorted by path),
write an ffmpeg concat list, and merge them into one output clip.

Usage:
    python combine_mp4s.py [root_dir] [output_file]

Defaults:
    root_dir    = current working directory
    output_file = combined_output.mp4
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path


def find_mp4s(root: str) -> list[Path]:
    """Recursively find all .mp4 files under root, sorted by full path."""
    mp4s = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for fname in filenames:
            if fname.lower().endswith(".mp4"):
                mp4s.append(Path(dirpath) / fname)
    return sorted(mp4s)


def check_ffmpeg() -> None:
    """Raise RuntimeError if ffmpeg is not on PATH."""
    result = subprocess.run(
        ["ffmpeg", "-version"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "ffmpeg not found. Install it with: sudo apt install ffmpeg  "
            "or  brew install ffmpeg"
        )


def write_concat_list(mp4s: list[Path], list_path: str) -> None:
    """Write an ffmpeg-style concat list file."""
    with open(list_path, "w", encoding="utf-8") as f:
        for p in mp4s:
            # ffmpeg concat demuxer requires forward slashes and escaped single quotes
            escaped = str(p.resolve()).replace("'", r"'\''")
            f.write(f"file '{escaped}'\n")


def combine(mp4s: list[Path], output: str) -> None:
    """Combine mp4s into a single file using ffmpeg concat demuxer."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, encoding="utf-8"
    ) as tmp:
        tmp_path = tmp.name

    try:
        write_concat_list(mp4s, tmp_path)

        cmd = [
            "ffmpeg",
            "-y",                      # overwrite output without asking
            "-f", "concat",
            "-safe", "0",              # allow absolute paths in the list
            "-i", tmp_path,
            "-c", "copy",              # stream-copy: no re-encode, very fast
            output,
        ]

        print(f"\nRunning: {' '.join(cmd)}\n")
        result = subprocess.run(cmd, check=False)

        if result.returncode != 0:
            raise RuntimeError(
                f"ffmpeg exited with code {result.returncode}. "
                "If clips have different codecs/resolutions, try removing "
                "'-c copy' to force re-encoding."
            )
    finally:
        os.unlink(tmp_path)


def main() -> None:
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    output = sys.argv[2] if len(sys.argv) > 2 else "combined_output.mp4"

    root = os.path.abspath(root)
    print(f"Scanning: {root}")

    check_ffmpeg()

    mp4s = find_mp4s(root)

    if not mp4s:
        print("No .mp4 files found.")
        return

    print(f"\nFound {len(mp4s)} .mp4 file(s):")
    for i, p in enumerate(mp4s, 1):
        print(f"  {i:>3}. {p}")

    combine(mp4s, output)
    print(f"\n✓ Combined clip saved to: {os.path.abspath(output)}")


if __name__ == "__main__":
    main()