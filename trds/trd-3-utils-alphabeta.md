# Technical Requirements Document: Utils — AlphaBeta

**Project:** ECE 479/579 Tic-Tac-Toe Solver
**Repository:** https://github.com/your-org/ece-579-alpha-beta-tic-tac-toe
**Date:** March 24, 2026
**Version:** 0.1.0

## 1. Overview

Implement the `AlphaBeta` utility class with static methods for alpha-beta pruning search. The key design feature is the `on_cutoff` callback parameter — cutoff events are reported to the caller rather than printed, keeping the utility side-effect-free and enabling the aggregate root pattern for cutoff collection.

## 2. Scope

### In Scope
- `AlphaBeta` class with two static methods in `app/utils/alphabeta.py`.
- Callback-based cutoff reporting via `on_cutoff` parameter.
- User-facing guide at `docs/guides/utils/alphabeta.md`.

### Out of Scope
- Domain objects for cutoff capture — covered in TRD 5.
- Minimax baseline — covered in TRD 2.

## 3. Components Affected

| Component | File/Path | Changes |
|-----------|-----------|---------|
| AlphaBeta | `app/utils/alphabeta.py` | New file — utility class |
| Guide | `docs/guides/utils/alphabeta.md` | New file — usage guide |

## 4. Detailed Requirements

### 4.1 Static Methods

- **`search(board, alpha, beta, is_maximizing, on_cutoff=None) -> Tuple[int, int]`** — Alpha-beta pruning search. When pruning occurs, calls `on_cutoff(board, cutoff_type)` if provided. `board` is the parent board state at the current recursive call. `cutoff_type` is `'Alpha cut'` or `'Beta cut'`.
- **`run(board: List[int], on_cutoff=None) -> Tuple[int, int]`** — Convenience wrapper that auto-detects the current player and initializes bounds to `±inf`.

### 4.2 Cutoff Semantics
- **Beta cutoff** (maximizing node): triggered when `alpha >= beta`.
- **Alpha cutoff** (minimizing node): triggered when `beta <= alpha`.
- The callback receives the board state at the node where pruning occurred (the parent), not the child that triggered the cutoff.

### 4.3 Dependencies
- Imports `BoardUtils` from `app.utils.board_utils`.

### 4.4 Code Style
- Artifact comments: `# *** utils` / `# ** util: alphabeta` / `# * method: search (static)`.
- RST docstrings on all methods.

## 5. Acceptance Criteria

1. `AlphaBeta.run(BoardUtils.parse_board('O_XOXX___'))` returns `(-1, 17)`.
2. Passing a list-appending lambda as `on_cutoff` collects 5 cutoff tuples for `O_XOXX___`.
3. Terminal boards return `(value, 1)` with no cutoff callbacks.
4. `on_cutoff=None` (default) produces no side effects.
5. All methods follow structured code style.
6. Guide document exists at `docs/guides/utils/alphabeta.md`.

## 6. Non-Functional Requirements

- No I/O, no printing — cutoffs reported only via callback.
- All methods are static.
- Depends only on `BoardUtils` — no framework imports.

## Related Code Style Documentation

- [code_style.md](https://github.com/greatstrength/tiferet/blob/v2.0-proto/docs/core/code_style.md)
