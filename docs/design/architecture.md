# Architecture (C4-style)

## Context (C4 Level 1)

Educators and tooling produce Python scene files. MotionGram reads them and writes MP4 (and optionally uses Kitten TTS models from the Hugging Face cache when the `tts` extra is installed).

## Containers (C4 Level 2)

```mermaid
flowchart TB
    subgraph devMachine [Dev_machine]
        ScenePy["scene_py"]
        CLI["motiongram_CLI"]
        Lib["motiongram_library"]
        Cache["cache_typst_svg_voices"]
        ScenePy --> CLI
        CLI --> Lib
        Lib --> Cache
    end
    MP4["output_mp4"]
    Lib --> MP4
```

- **CLI** — thin Typer wrapper: parse args, import scene, invoke pipeline.
- **Library** — scene graph, timeline, render, export, audio.
- **Cache** — disk cache under user home (XDG-style path TBD).

## Components (C4 Level 3)

```mermaid
flowchart LR
    Core["core_Scene_Node_Timeline"]
    Prim["shapes_text"]
    Anim["animate_easing"]
    Rend["render_Skia"]
    Typst["Typst_tool"]
    Exp["export_PyAV"]
    Aud["audio_mixer_voiceover"]

    Core --> Prim
    Core --> Anim
    Prim --> Rend
    Anim --> Rend
    Prim --> Typst
    Typst -->|SVG| Rend
    Rend --> Exp
    Aud --> Exp
```

## Key data flow

1. **Authoring time:** build `Scene`, attach `Node` tree, append `Timeline` entries.
2. **Render time:** for each `t`, evaluate active animators, update node state (implementation detail: mutable scratch state vs pure — TBD in implementation ADR).
3. **Encode time:** push RGB frames + PCM/WAV into PyAV muxer.

## Related documents

- [data-model.md](data-model.md)
- [rendering-pipeline.md](rendering-pipeline.md)
- [voiceover-adapter.md](voiceover-adapter.md)
