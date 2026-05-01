# Principles examples

Scripts in [`examples/principles/`](../../examples/principles/) illustrate drawing and animation fundamentals. Each file is self-contained: run it from the repo root with Python and it encodes an MP4 **next to the script** (those outputs are gitignored).

```bash
cd /path/to/Typmotion
python examples/principles/04_value.py
# produces examples/principles/04_value.mp4
```

Requires the same setup as the rest of Typmotion ([Setup Guide](setup.md)): editable install, skia-python, PyAV, optional Typst for math-heavy scenes.

## Drawing principles (01–12)

| Script | Topic |
|--------|--------|
| `01_line.py` | Line |
| `02_shape.py` | Shape |
| `03_form.py` | Form |
| `04_value.py` | Value (gradient, shadow) |
| `05_space.py` | Space |
| `06_perspective.py` | Perspective |
| `07_proportion.py` | Proportion |
| `08_anatomy.py` | Anatomy |
| `09_composition.py` | Composition |
| `10_contrast.py` | Contrast |
| `11_edge_control.py` | Edge control |
| `12_gesture.py` | Gesture |

## Animation principles (13–24)

| Script | Topic |
|--------|--------|
| `13_squash_stretch.py` | Squash & stretch |
| `14_anticipation.py` | Anticipation |
| `15_staging.py` | Staging |
| `16_straight_pose.py` | Straight ahead / pose to pose |
| `17_follow_through.py` | Follow through & overlapping |
| `18_slow_in_out.py` | Slow in & slow out |
| `19_arcs.py` | Arcs |
| `20_secondary_action.py` | Secondary action |
| `21_timing.py` | Timing |
| `22_exaggeration.py` | Exaggeration |
| `23_solid_drawing.py` | Solid drawing |
| `24_appeal.py` | Appeal |

For authoring conventions (timeline vs `Node.update`, composable animators), see [`AGENTS.md`](../../AGENTS.md).
