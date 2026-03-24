# Technical Requirements Document: Events — SolveTicTacToe & PrintResults

**Project:** ECE 479/579 Tic-Tac-Toe Solver
**Repository:** https://github.com/your-org/ece-579-alpha-beta-tic-tac-toe
**Date:** March 24, 2026
**Version:** 0.1.0

## 1. Overview

Implement two chained domain events in a single module. `SolveTicTacToe` orchestrates both search algorithms and collects results via the aggregate root pattern. `PrintResults` reads the stored results and formats output per the homework specification. The events are chained via Tiferet's `data_key` mechanism — computation and presentation are cleanly separated.

## 2. Scope

### In Scope
- `SolveTicTacToe` and `PrintResults` domain events in `app/events/tictactoe.py`.
- Package init file `app/events/__init__.py`.
- User-facing guide at `docs/guides/events/tictactoe.md`.

### Out of Scope
- Utility implementations — covered in TRDs 1–3.
- Domain objects and aggregate — covered in TRDs 4–5.
- Tiferet config wiring — covered in TRD 7.

## 3. Components Affected

| Component | File/Path | Changes |
|-----------|-----------|---------|
| SolveTicTacToe | `app/events/tictactoe.py` | New domain event |
| PrintResults | `app/events/tictactoe.py` | New domain event |
| Package init | `app/events/__init__.py` | New file — empty |
| Guide | `docs/guides/events/tictactoe.md` | New file — usage guide |

## 4. Detailed Requirements

### 4.1 SolveTicTacToe

- **Decorator:** `@DomainEvent.parameters_required(['board'])`
- **Validation:**
  - Board length must be exactly 9 (`self.verify`, error code `INVALID_INPUT`).
  - Board characters must be in `{X, O, _}` (`self.verify`, error code `INVALID_INPUT`).
- **Execution:**
  1. Parse board via `BoardUtils.parse_board()`.
  2. Run `Minimax.run()` → create `GameResultAggregate` with minimax results.
  3. Create second `GameResultAggregate` for alphabeta (placeholder values, `validate=False`).
  4. Run `AlphaBeta.run()` with `aggregate.record_cutoff` as `on_cutoff`.
  5. Update alphabeta aggregate via `set_attribute('value', ...)` and `set_attribute('nodes', ...)`.
  6. Return dict: `{board, minimax_result, alphabeta_result}`.
- **Feature config** stores this dict via `data_key: results`.

### 4.2 PrintResults

- **Decorator:** `@DomainEvent.parameters_required(['results'])`
- **Output format (in order):**
  1. Initial board (3 rows via `BoardUtils.format_board()`).
  2. `Game Result: {value}` + `Moves considered without alpha-beta pruning: {nodes}`.
  3. For each cutoff: board (3 rows) + cutoff type, blank line between cutoffs.
  4. `Game Result: {value}` + `Moves considered with alpha-beta pruning: {nodes}` + `Alpha cuts: {n}` + `Beta cuts: {n}`.
- Returns empty string to suppress CLI `None` output.

### 4.3 Dependencies
- `BoardUtils`, `Minimax`, `AlphaBeta` from `app.utils`.
- `GameResultAggregate` from `app.mappers.result`.
- `DomainEvent`, `Aggregate` from `tiferet`.

### 4.4 Code Style
- Artifact comments: `# *** events` / `# ** event: solve_tic_tac_toe` / `# ** event: print_results`.
- RST docstrings on `execute` methods.

## 5. Acceptance Criteria

1. `python tictactoe_cli.py tictactoe solve O_XOXX___` produces correct output with board, minimax stats, cutoff blocks, and alphabeta stats.
2. Invalid board input (`BAD`) raises `INVALID_INPUT` error.
3. Terminal board (`XOXOXOXOX`) produces `Game Result: 1`, 1 node, 0 cuts.
4. No `None` appears in CLI output.
5. Both events follow structured code style.
6. Guide document exists at `docs/guides/events/tictactoe.md`.

## 6. Non-Functional Requirements

- `SolveTicTacToe` performs no I/O — all output is in `PrintResults`.
- Events are loosely coupled via `data_key` — either can be replaced independently.
- Consistent with Tiferet structured code style.

## Related Code Style Documentation

- [code_style.md](https://github.com/greatstrength/tiferet/blob/v2.0-proto/docs/core/code_style.md)
- [events.md](https://github.com/greatstrength/tiferet/blob/v2.0-proto/docs/core/events.md)
