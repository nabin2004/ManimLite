# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `learn/` tutorial: 101 phase markdown files (`000`–`100`) building the engine concept from a print renderer to PyAV-oriented architecture.

### Changed

- Optional voice-over stack: **Piper** (`piper-tts`, GPL) replaced by **Kitten TTS** (Apache-2.0) behind the `[tts]` extra; default voice `Jasper`; default backend `KittenVoiceOverBackend`.

### Added (earlier)

- Repository scaffold: `src/manimlite` package stubs, tests layout, CI skeleton.
- SDRE documentation: SRS, SDD, supporting design docs, ADRs, proposal, roadmap.
