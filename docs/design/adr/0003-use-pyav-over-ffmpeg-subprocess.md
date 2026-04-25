# ADR-0003: Use PyAV (in-process libav) instead of per-frame ffmpeg subprocess

- **Status:** Accepted
- **Date:** 2025-04-25

## Context

Disk-based frame pipelines plus external ffmpeg invocations add latency and I/O overhead, especially on cloud disks.

## Decision

Encode video using **PyAV** in-process, streaming frames directly into the muxer **without** writing intermediate frame files in the default configuration.

## Consequences

- **Positive:** Lower overhead; better control over timestamps and mux.
- **Negative:** Requires compatible libav at runtime; debugging is less “shell-transparent” than ffmpeg CLI.
- **Follow-up:** Optional debug mode to dump frames remains possible but off by default.
