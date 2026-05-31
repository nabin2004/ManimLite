# MotionGram 📽️ — learn path (phases 000–100)

Files use **three-digit** prefixes (`000_` … `100_`) so they sort correctly beside `100_…`.

This folder is a **step-by-step tutorial** that builds a lightweight animation engine from a print-based canvas to a near-production design. Read files **in numeric order**; each one adds a small concept. Requirements/design specs live in [docs/](../docs/).

## Bands

| Band | Phases | Theme |
|------|--------|--------|
| A | [000](000_overview.md)–[010](010_first_node_class.md) | Procedural drawing; why `Node` appears |
| B | [011](011_node_draw.md)–[030](030_save_frame_png.md) | `Scene`, shapes, polymorphism, numpy, PNG |
| C | [031](031_what_is_animation_lerp.md)–[050](050_from_frames_to_video_concept.md) | Animations, timeline, easing, frame loop |
| D | [051](051_transform_dataclass.md)–[070](070_testing_strategy.md) | Transforms, `Group`, `Renderer` protocol, tests |
| E | [071](071_architecture_recap.md)–[090](090_packaging_lockfile.md) | PyAV, audio, perf, CLI, `pyproject` |
| F | [091](091_distribution.md)–[100](100_final_architecture.md) | Plugins, extensibility, final architecture |

## Phase index

- [000 — Overview](000_overview.md) · [001 — Motivation](001_motivation.md) · [002 — Design philosophy](002_design_philosophy.md)
- [003 — Python / uv setup](003_python_setup.md) · [004 — Canvas and coordinates](004_canvas_and_coordinates.md) · [005 — Print renderer](005_print_renderer.md)
- [006 — Draw a point](006_draw_point.md) · [007 — Draw a line](007_draw_line.md) · [008 — Draw a circle](008_draw_circle.md) · [009 — Limits of functions](009_limits_of_functions.md)
- [010 — First `Node` class](010_first_node_class.md) · [011 — `Node.draw()`](011_node_draw.md) · [012 — Node position](012_node_position.md)
- [013 — List of nodes vs Scene](013_list_vs_scene.md) · [014 — `Scene` class](014_scene_class.md) · [015 — `Scene.render()`](015_scene_render.md)
- [016 — `Circle` shape](016_circle_shape.md) · [017 — `Line` shape](017_line_shape.md) · [018 — `Rectangle` shape](018_rectangle_shape.md) · [019 — Duplication smell](019_duplication_smell.md)
- [020 — Base `Shape`](020_base_shape.md) · [021 — Polymorphic draw](021_polymorphic_draw.md) · [022 — `Drawable` protocol](022_drawable_protocol.md) · [023 — Color and stroke](023_color_stroke.md) · [024 — Z-ordering](024_z_ordering.md)
- [025 — Grouping with children](025_grouping_children.md) · [026 — Recursive draw](026_recursive_draw.md) · [027 — Limits of ASCII](027_limits_of_ascii.md) · [028 — NumPy framebuffer](028_numpy_framebuffer.md) · [029 — `draw` into array](029_draw_into_array.md) · [030 — Save frame PNG](030_save_frame_png.md)
- [031 — Lerp and `t`](031_what_is_animation_lerp.md) · [032 — `Move` animation class](032_move_animation.md) · [033 — Apply over frames](033_apply_over_frames.md) · [034 — Fade in/out](034_fade_animation.md) · [035 — Scale animation](035_scale_animation.md) · [036 — Many animations, one node](036_multiple_animations.md) · [037 — Timeline tuples](037_timeline_tuples.md) · [038 — `Scene` records entries](038_scene_animate.md) · [039 — Sequential vs parallel](039_sequential_parallel.md) · [040 — Easing](040_easing.md) · [041 — Ease in animators](041_easing_in_animators.md) · [042 — Dispatcher loop](042_dispatcher_loop.md) · [043 — Subclass explosion](043_subclass_explosion.md) · [044 — Callable animator](044_callable_animator.md) · [045 — Dataclass animators](045_dataclass_animators.md) · [046 — Generic tween](046_generic_tween.md) · [047 — Property-based animation](047_property_animations.md) · [048 — `Scene.play()`](048_scene_play.md) · [049 — N frames](049_render_n_frames.md) · [050 — From frames to video](050_from_frames_to_video_concept.md)
- [051 — `Transform` dataclass](051_transform_dataclass.md) · [052 — Replace raw `x, y`](052_replace_xy_with_transform.md) · [053 — Compose transforms](053_compose_transforms.md) · [054 — Parent chain](054_parent_transform_chain.md) · [055 — `Group`](055_group_node.md) · [056 — Shape = geometry + style + transform](056_shape_refactor.md) · [057 — `Style` dataclass](057_style_dataclass.md) · [058 — Composition proof](058_composition_over_inheritance.md) · [059 — Traversal](059_scene_graph_traversal.md) · [060 — Bounding box](060_bounding_box.md) · [061 — Dirty flags](061_dirty_flags.md) · [062 — `Renderer` protocol](062_renderer_protocol.md) · [063 — `NumpyRenderer`](063_numpy_renderer.md) · [064 — Skia sketch](064_skia_sketch.md) · [065 — Renderer vs exporter](065_renderer_vs_exporter.md) · [066 — Frame iterator](066_frame_iterator.md) · [067 — Time-driven loop](067_time_driven_loop.md) · [068 — `Scene.save` API](068_scene_save_api.md) · [069 — Error handling](069_error_handling.md) · [070 — Testing strategy](070_testing_strategy.md)
- [071 — Architecture recap](071_architecture_recap.md) · [072 — Profiling](072_profiling.md) · [073 — No disk frame dump](073_no_disk_frame_pipeline.md) · [074 — PyAV intro](074_pyav_intro.md) · [075 — H264 stream](075_pyav_h264_stream.md) · [076 — PCM timeline](076_pcm_timeline.md) · [077 — Mux audio video](077_mux_audio_video.md) · [078 — Voiceover hook](078_voiceover_hook.md) · [079 — Kitten TTS optional](079_kitten_tts_hook.md) · [080 — pydub mix](080_pydub_mix.md) · [081 — Math cache (Typst concept)](081_math_cache_typst.md) · [082 — Font cache](082_font_caching.md) · [083 — Chunked encoding](083_memory_chunked_encoding.md) · [084 — Determinism](084_determinism.md) · [085 — Async and threads](085_async_threading.md) · [086 — CLI `render`](086_cli_render.md) · [087 — Scene discovery](087_scene_discovery.md) · [088 — Config](088_config.md) · [089 — Debug overlay](089_debug_overlay.md) · [090 — Packaging and lockfile](090_packaging_lockfile.md)
- [091 — Distribution](091_distribution.md) · [092 — Plugin shapes](092_plugin_shapes.md) · [093 — Pluggable renderers](093_pluggable_renderers.md) · [094 — Pluggable animators](094_pluggable_animators.md) · [095 — Pluggable voice backends](095_pluggable_voiceover.md) · [096 — CI recap](096_ci_and_tests.md) · [097 — AGENTS and LLM](097_agents_llm.md) · [098 — vs ManimCE](098_manimce_comparison.md) · [099 — Limitations](099_limitations.md) · [100 — Final architecture](100_final_architecture.md)

## How to use the code

Each phase file contains **illustrative** code. You can copy it into a single `python phase_XXX.py` file as you go, or keep one evolving `toy_manim.py` and refactor when the text tells you to. The goal is **understanding the progression**, not a perfect library until the end.
