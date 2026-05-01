# Contributing to ManimLite

Thank you for your interest in ManimLite.

## Development setup

1. Install [uv](https://docs.astral.sh/uv/).
2. Clone the repository and run:

   ```bash
   uv sync --extra dev --extra tts
   ```

3. Run checks:

   ```bash
   uv run ruff check src tests
   uv run mypy src
   uv run pytest
   ```

## Guidelines

- Prefer **flat, typed, dataclass-oriented** public APIs (see [AGENTS.md](AGENTS.md)).
- Keep the **install footprint** and **cold start** goals in mind when adding dependencies.
- Add or update **requirements traceability** in [docs/requirements/SRS.md](docs/requirements/SRS.md) when changing behavior.
- For architectural shifts, add an **ADR** under [docs/design/adr/](docs/design/adr/).
- **Tracked video:** keep repository binaries small. Only commit short demos under `docs/assets/` (see [docs/assets/README.md](docs/assets/README.md)); other renders stay gitignored.

## Pull requests

- One logical change per PR when possible.
- Include tests for new behavior once the implementation exists.
- Update `CHANGELOG.md` under **Unreleased** for user-visible changes.
