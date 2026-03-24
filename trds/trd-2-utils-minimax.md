# Technical Requirements Document: Utils — Minimax

**Project:** ECE 479/579 Tic-Tac-Toe Solver
**Repository:** https://github.com/your-org/ece-579-alpha-beta-tic-tac-toe
**Date:** March 24, 2026
**Version:** 0.1.0

## 1. Overview

Implement the `Minimax` utility class with static methods for plain recursive minimax search. This serves as the baseline algorithm against which Alpha-Beta pruning is compared.

## 2. Scope

### In Scope
- `Minimax` class with two static methods in `app/utils/minimax.py`.
- User-facing guide at `docs/guides/utils/minimax.md`.

### Out of Scope
- Alpha-Beta pruning — covered in TRD 3.
- Board utilities — covered in TRD 1.

## 3. Components Affected

| Component | File/Path | Changes |
|-----------|-----------|---------|
| Minimax | `app/utils/minimax.py` | New file — utility class |
| Guide | `docs/guides/utils/minimax.md` | New file — usage guide |

## 4. Detailed Requirements

### 4.1 Static Methods

- **`search(board: List[int], is_maximizing: bool) -> Tuple[int, int]`** — Full recursive minimax. Returns `(utility_value, node_count)`. Every recursive call (internal + terminal) counts as one node.
- **`run(board: List[int]) -> Tuple[int, int]`** — Convenience wrapper that auto-detects the current player via `BoardUtils.current_player()` and calls `search()`.

### 4.2 Dependencies
- Imports `BoardUtils` from `app.utils.board_utils`.
- Uses `BoardUtils.is_terminal`, `BoardUtils.utility`, `BoardUtils.get_successors`, `BoardUtils.current_player`.

### 4.3 Code Style
- Artifact comments: `# *** utils` / `# ** util: minimax` / `# * method: search (static)`.
- RST docstrings on all methods.

## 5. Acceptance Criteria

1. `Minimax.run(BoardUtils.parse_board('O_XOXX___'))` returns `(-1, 26)`.
2. `Minimax.run(BoardUtils.parse_board('XOXOXOXOX'))` returns `(1, 1)` for a terminal board.
3. Node count includes both internal and terminal nodes.
4. All methods follow structured code style.
5. Guide document exists at `docs/guides/utils/minimax.md`.

## 6. Non-Functional Requirements

- No I/O, no side effects.
- All methods are static.
- Depends only on `BoardUtils` — no framework imports.

## Related Code Style Documentation

- [code_style.md](https://github.com/greatstrength/tiferet/blob/v2.0-proto/docs/core/code_style.md)
