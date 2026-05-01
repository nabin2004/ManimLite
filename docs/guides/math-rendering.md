# Math Rendering with Typst

ManimLite uses [Typst](https://typst.app/) instead of LaTeX for math typesetting.
This makes the toolchain dramatically smaller and faster than ManimCE's LaTeX
dependency (no TeX Live install needed).

## How It Works

```
MathExpr(typst_source="...") → typst_cache.py → typst CLI → .svg file → Skia SVGDOM → canvas
```

1. **`MathExpr`** nodes hold a `typst_source` string (Typst math syntax).
2. At draw time, `MathExpr.draw()` calls `cached_typst_svg_path()`.
3. The cache hashes the source, checks `~/.cache/manimlite/typst/` for an
   existing SVG, and compiles via `typst compile` only on cache miss.
4. The SVG bytes are passed to `SkiaCanvas.draw_svg_bytes()`, which uses
   `skia.SVGDOM` to rasterize directly onto the Skia canvas.

## Typst Math Syntax

Typst math syntax differs from LaTeX. Key differences:

| LaTeX | Typst | Notes |
|-------|-------|-------|
| `\frac{a}{b}` | `a / b` | Fractions are just division |
| `\sum_{i=0}^{n}` | `sum_(i=0)^n` | Subscript with `_()`, superscript with `^` |
| `\alpha` | `alpha` | No backslash needed |
| `\sqrt{x}` | `sqrt(x)` | Function call syntax |
| `\int_a^b` | `integral_a^b` | Spelled out |
| `\mathbb{R}` | `RR` | Double letters for blackboard bold |
| `\left( \right)` | `( )` | Auto-sizing by default |

## Usage

```python
from manimlite import Scene, MoveX
from manimlite.text import MathExpr

scene = Scene(width=1280, height=720, fps=30.0, duration=3.0)

expr = MathExpr(
    typst_source="integral_0^infinity e^(-x^2) dif x = sqrt(pi) / 2",
    x=100,
    y=300,
    font_size=36.0,
    color="#FFFFFF",
)
scene.add_node(expr)
scene.add_animation(0.0, 2.0, expr, MoveX(100.0, 400.0))
```

## Cache Configuration

The Typst SVG cache lives at `~/.cache/manimlite/typst/` by default.
Override with:

```bash
export MANIMLITE_CACHE_HOME=/path/to/cache
```

Cache files are named by SHA-256 hash of the source, so identical expressions
always reuse the same SVG.

## Limitations

- Typst syntax only (no LaTeX compatibility layer).
- The `typst` CLI binary must be on `PATH`.
- SVG rendering quality depends on Skia's SVGDOM support.
- Color is applied at the Skia level, not inside the Typst document.

## Related

- [ADR-0002: Use Typst over LaTeX](../design/adr/0002-use-typst-over-latex.md)
- [Rendering Pipeline](../design/rendering-pipeline.md)
- [Typst documentation](https://typst.app/docs/)
