# DSA used in src/motiongram

This file lists the main algorithms and data-structure concepts used inside the `src/motiongram` package.

## Direct runtime usage

| Concept | File(s) | Notes |
|---|---|---|
| Scene graph tree | `src/motiongram/core.py` | `Node.children` forms a tree, and drawing/update logic walks it recursively.
| Depth-first traversal | `src/motiongram/core.py` | Parent nodes visit children in recursive order during render/update passes.
| Stack-based state | `src/motiongram/render.py` | Skia canvas state uses push/pop stacks for nested transforms, alpha, and blur.
| Linear interpolation | `src/motiongram/animate.py` | `lerp()` is the core numeric primitive for motion, scaling, and rotation.
| Hermite smoothing | `src/motiongram/animate.py` | `smoothstep()` provides eased interpolation over normalized time.
| Timeline scheduling | `src/motiongram/core.py`, `src/motiongram/animate.py` | Animation entries are ordered tuples with start/end times and target nodes.
| Animator composition | `src/motiongram/animate.py` | `Parallel`, `Sequence`, and `Delay` combine animators into behavior trees.
| Bresenham line algorithm | `src/motiongram/renderer.py` | Used by the ASCII renderer for raster line drawing.
| Midpoint circle algorithm | `src/motiongram/renderer.py` | Used by the ASCII renderer for raster circle drawing.
| Cubic Bézier evaluation | `src/motiongram/easing.py` | Used for easing curves and curve-based timing.
| Binary search | `src/motiongram/easing.py` | `cubic_bezier()` searches for the Bézier parameter whose x-value matches progress.
| Polynomial easing | `src/motiongram/easing.py` | Quad, cubic, and back easing functions shape motion curves.
| Trigonometric easing | `src/motiongram/easing.py` | Elastic easing uses sine/exponential behavior for overshoot and settling.
| Piecewise easing | `src/motiongram/easing.py` | Bounce easing is implemented with multiple interval branches.
| Subtitle sorting | `src/motiongram/subtitles.py` | Cues are sorted with a multi-field key before rendering/export.
| Subtitle filtering | `src/motiongram/subtitles.py` | Active cues are selected by interval containment at time `t`.
| Path sampling | `src/motiongram/composition.py` | Spiral and gesture helpers approximate curves by sampling points.
| Curve stitching | `src/motiongram/composition.py`, `src/motiongram/shapes.py` | Bézier control points are used to construct smooth paths and curves.
| Deterministic procedural generation | `src/motiongram/procedural/rainy_landscape.py` | Seeded randomness is used to make generated scenes repeatable.

## Per-shape algorithms

Below are the primary algorithms or techniques used when rendering or constructing common shapes in `src/motiongram`.

- Line: Bresenham line algorithm for ASCII raster (`src/motiongram/renderer.py`); vector line via backend path APIs for Skia.
- Circle / SemiCircle / Sector: Midpoint circle algorithm for ASCII raster (`src/motiongram/renderer.py`); vector arcs/fills via Skia path primitives.
- BezierCurve / Path / GesturePath: Cubic Bézier segments; Skia uses `cubicTo` for vector stroking; curve sampling and stitching used for gesture ribbons (`src/motiongram/composition.py`, `src/motiongram/shapes.py`).
- Arc: sampled circular arc for ASCII; native arc stroking in Skia (`src/motiongram/shapes.py`, `src/motiongram/render.py`).
- Ellipse: parametric sampling for raster/backends or backend ellipse primitives (`src/motiongram/shapes.py`).
- Polygon / RegularPolygon: vertex generation with trig (cos/sin) and polygon fill via backend (`src/motiongram/shapes.py`).
- Rectangle / Rounded rectangle: rectangle fill and optional corner radius via backend path primitives (`src/motiongram/shapes.py`).
- Path sampling / Curve stitching: helpers create sampled points from analytic curves (GoldenSpiral, GesturePath) and either stroke as Béziers or approximate with polylines (`src/motiongram/composition.py`).
- MoveAlongPath / polyline helpers: polyline length accumulation and parameterization for constant-speed travel along a sampled polyline (`src/motiongram/animate.py`).

