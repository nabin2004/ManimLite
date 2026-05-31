# Setup Guide

This guide covers installing MotionGram's two core external dependencies:
**skia-python** (2D rendering) and **Typst** (math typesetting).

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## 1. System Dependencies (Linux)

skia-python requires OpenGL and fontconfig libraries:

```bash
# Ubuntu / Debian
sudo apt-get install -y \
    libfontconfig1 libgl1-mesa-glx libgl1-mesa-egl \
    libegl1 libglvnd0 libgl1-mesa-dri

# Fedora / RHEL
sudo yum install -y \
    fontconfig mesa-libGL mesa-libEGL \
    libglvnd-egl mesa-dri-drivers
```

macOS and Windows users get these bundled with skia-python wheels.

## 2. Install skia-python

skia-python is declared as a project dependency and installs automatically:

```bash
uv pip install -e ".[dev]"
# or: pip install -e ".[dev]"
```

Verify:

```python
import skia
surface = skia.Surface(64, 64)
print("skia-python OK")
```

## 3. Install Typst CLI

MotionGram uses Typst as a CLI tool (invoked via subprocess) to compile math
expressions into SVG. Install the binary:

### Option A: Pre-built binary (recommended)

```bash
mkdir -p ~/.local/bin
curl -fsSL \
  https://github.com/typst/typst/releases/latest/download/typst-x86_64-unknown-linux-musl.tar.xz \
  | tar -xJ --strip-components=1 -C ~/.local/bin/
```

For macOS (Apple Silicon):

```bash
brew install typst
```

### Option B: Via Cargo

```bash
cargo install --locked typst-cli
```

### Verify

```bash
typst --version
# Expected: typst 0.14.x or later
```

Ensure `typst` is on your `PATH`. MotionGram's `typst_cache.py` uses
`shutil.which("typst")` to locate the binary.

## 4. Verify the Full Pipeline

```bash
# From the project root
python examples/math_and_text.py
# Should produce math_and_text.mp4
```

Or via the CLI:

```bash
motiongram render examples/math_and_text.py -o output.mp4
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: No module named 'skia'` | `uv pip install skia-python` |
| `typst: command not found` | Install Typst and add its directory to `PATH` |
| `libEGL.so: cannot open shared object` | Install `libegl1` (Ubuntu) or `mesa-libEGL` (Fedora) |
| Math expressions render as blank | Check `typst --version` works; check `~/.cache/motiongram/typst/` for cached SVGs |
| `TypeError: MakeLinear(): incompatible function arguments` | Upgrade MotionGram — linear gradients pass a **sequence** of two `skia.Point`s per current skia-python bindings; ensure `skia-python>=120` per `pyproject.toml`. |

## Optional: custom Skia background in the CLI

Scene modules may define:

```python
def get_skia_renderer() -> SkiaRenderer:
    return SkiaRenderer(clear_color=(18, 22, 32))
```

`motiongram render` calls it when present so MP4 matches `python your_scene.py`.

## 5. Principles gallery

Short drawing and animation demos live in `examples/principles/`. Run any script from the repo root; it writes `<name>.mp4` beside the script:

```bash
python examples/principles/04_value.py
```

See [Principles examples](principles-examples.md) for the full index.

