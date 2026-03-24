# Technical Requirements Document: Utils — BoardUtils

**Project:** ECE 479/579 Tic-Tac-Toe Solver
**Repository:** https://github.com/your-org/ece-579-alpha-beta-tic-tac-toe
**Date:** March 24, 2026
**Version:** 0.1.0

## 1. Overview

Implement the `BoardUtils` utility class with static methods for all tic-tac-toe board operations: parsing, formatting, successor generation, terminal detection, utility evaluation, and player detection. This is the foundational utility upon which both search algorithms depend.

## 2. Scope

### In Scope
- `BoardUtils` class with six static methods in `app/utils/board_utils.py`.
- Module-level constants (`CELL_MAP`, `CELL_DISPLAY`, `WIN_LINES`).
- User-facing guide at `docs/guides/utils/board_utils.md`.
- Package init file `app/utils/__init__.py`.

### Out of Scope
- Search algorithms (Minimax, AlphaBeta) — covered in TRD 2 and TRD 3.
- Domain objects — covered in TRD 4 and TRD 5.

## 3. Components Affected

| Component | File/Path | Changes |
|-----------|-----------|---------|
| BoardUtils | `app/utils/board_utils.py` | New file — utility class |
| Package init | `app/utils/__init__.py` | New file — empty |
| Guide | `docs/guides/utils/board_utils.md` | New file — usage guide |

## 4. Detailed Requirements

### 4.1 Constants
- `CELL_MAP = {'X': 1, 'O': -1, '_': 0}` — string-to-int mapping.
- `CELL_DISPLAY = {1: 'X', -1: 'O', 0: '_'}` — int-to-string mapping.
- `WIN_LINES` — 8 tuples representing all winning index combinations.

### 4.2 Static Methods

All methods are `@staticmethod` on `BoardUtils`.

- **`parse_board(board_str: str) -> List[int]`** — Converts 9-char string to list of ints.
- **`format_board(board: List[int]) -> str`** — Returns 3-line display string (no printing).
- **`get_successors(board: List[int], player: int) -> List[Tuple[int, List[int]]]`** — Returns `(move_index, new_board)` for each empty cell.
- **`is_terminal(board: List[int]) -> bool`** — Checks win or full board.
- **`utility(board: List[int]) -> int`** — Returns `1` (X wins), `-1` (O wins), `0` (draw).
- **`current_player(board: List[int]) -> int`** — Returns `1` when X/O counts are equal, `-1` otherwise.

### 4.3 Code Style
- Artifact comments: `# *** utils` / `# ** util: board_utils` / `# * method: <name> (static)`.
- RST docstrings on all methods.

## 5. Acceptance Criteria

1. `BoardUtils.parse_board('O_XOXX___')` returns `[-1, 0, 1, -1, 1, 1, 0, 0, 0]`.
2. `BoardUtils.format_board([-1, 0, 1, -1, 1, 1, 0, 0, 0])` returns `'O_X\nOXX\n___'`.
3. `BoardUtils.is_terminal` correctly identifies wins, draws, and ongoing games.
4. `BoardUtils.current_player` returns `1` when piece counts are equal.
5. All methods follow structured code style with artifact comments.
6. Guide document exists at `docs/guides/utils/board_utils.md`.

## 6. Non-Functional Requirements

- No I/O, no framework imports, no side effects.
- All methods are static — no instance state.
- Consistent with Tiferet structured code style.

## Related Code Style Documentation

- [code_style.md](https://github.com/greatstrength/tiferet/blob/v2.0-proto/docs/core/code_style.md)
