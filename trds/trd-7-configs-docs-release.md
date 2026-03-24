# Technical Requirements Document: Configs, Docs & v0.1.0 Release

**Project:** ECE 479/579 Tic-Tac-Toe Solver
**Repository:** https://github.com/your-org/ece-579-alpha-beta-tic-tac-toe
**Date:** March 24, 2026
**Version:** 0.1.0

## 1. Overview

Wire the full Tiferet application via YAML configurations, create the CLI entry point, set up project metadata with dynamic versioning, and produce the README and AGENTS.md documentation. This TRD brings together all prior implementation work (TRDs 1–6) into a runnable, documented release.

## 2. Scope

### In Scope
- All YAML config files in `app/configs/`.
- CLI entry point `tictactoe_cli.py`.
- Project metadata `pyproject.toml` with dynamic version from `app/__init__.py`.
- Version variable in `app/__init__.py`.
- `README.md` — user-facing project documentation.
- `AGENTS.md` — contributor and AI agent guidance.

### Out of Scope
- Implementation of utils, domain, mappers, events — covered in TRDs 1–6.

## 3. Components Affected

| Component | File/Path | Changes |
|-----------|-----------|---------|
| App config | `app/configs/app.yml` | New — interface definitions |
| CLI config | `app/configs/cli.yml` | New — command structure |
| Container config | `app/configs/container.yml` | New — event registration |
| Error config | `app/configs/error.yml` | New — INVALID_INPUT error |
| Feature config | `app/configs/feature.yml` | New — chained event workflow |
| Logging config | `app/configs/logging.yml` | New — WARNING level, root logger |
| Package init | `app/configs/__init__.py` | New — empty |
| Version | `app/__init__.py` | New — `__version__ = '0.1.0'` |
| Entry point | `tictactoe_cli.py` | New — CLI runner |
| Metadata | `pyproject.toml` | New — dynamic version from `app.__version__` |
| README | `README.md` | Updated — full documentation |
| AGENTS | `AGENTS.md` | New — agent/contributor guidance |

## 4. Detailed Requirements

### 4.1 Configs

**app.yml** — Two interfaces: `basic_tictactoe` (default) and `tictactoe_cli` (CliContext with CliYamlProxy + CliHandler).

**cli.yml** — One command group `tictactoe` with subcommand `solve` accepting positional arg `board`.

**container.yml** — Two attrs: `solve_tictactoe_evt` → `app.events.tictactoe.SolveTicTacToe`, `print_results_evt` → `app.events.tictactoe.PrintResults`.

**error.yml** — `INVALID_INPUT` error with `en_US` message template.

**feature.yml** — Feature `tictactoe.solve` chains two commands: `solve_tictactoe_evt` (with `data_key: results`) → `print_results_evt`.

**logging.yml** — Default formatter, console handler at WARNING level, root logger at WARNING.

### 4.2 Entry Point

`tictactoe_cli.py` — Loads `tictactoe_cli` interface via `App().load_interface()` and calls `cli.run()`.

### 4.3 Project Metadata

`pyproject.toml` — Uses `setuptools>=64` build backend. Version is dynamic, sourced from `app.__version__` via `[tool.setuptools.dynamic]`.

`app/__init__.py` — Exports `__version__ = '0.1.0'`.

### 4.4 Documentation

**README.md** — Quick start, board format, example output, architecture overview with tree, design highlights, development prerequisites, guide links.

**AGENTS.md** — Project overview, architecture (layer overview, key design decisions, runtime flow), structured code style (comment levels, spacing, docstrings), component reference, board representation, extension patterns, conventions summary.

## 5. Acceptance Criteria

1. `python tictactoe_cli.py tictactoe solve O_XOXX___` produces correct, clean output.
2. Invalid input (`BAD`) produces `INVALID_INPUT` error message and exits with code 1.
3. No INFO/DEBUG log lines appear in normal output.
4. `pyproject.toml` resolves version `0.1.0` from `app.__version__`.
5. README contains architecture tree, example output, and guide links.
6. AGENTS.md covers all components and conventions.

## 6. Non-Functional Requirements

- CLI output is clean — no framework noise, no trailing `None`.
- All configs follow Tiferet YAML conventions.
- Documentation is accurate and reflects the final implementation.

## Related Code Style Documentation

- [code_style.md](https://github.com/greatstrength/tiferet/blob/v2.0-proto/docs/core/code_style.md)
