# BoardUtils

**Module:** `app/utils/board_utils.py`

Board manipulation utilities for tic-tac-toe. All methods are static — no state, no I/O, no framework dependencies.

## Board Representation

- **String format** (CLI input): 9 characters using `X`, `O`, `_` — read left-to-right, top-to-bottom.
- **Internal format**: `List[int]` — `1` = X, `-1` = O, `0` = empty.

## Constants

- `CELL_MAP` — Maps characters to integers: `{'X': 1, 'O': -1, '_': 0}`
- `CELL_DISPLAY` — Maps integers to characters: `{1: 'X', -1: 'O', 0: '_'}`
- `WIN_LINES` — All 8 winning combinations (3 rows, 3 columns, 2 diagonals) as index tuples.

## Methods

### `parse_board(board_str: str) -> List[int]`

Converts a 9-character board string to a list of integers.

```python
BoardUtils.parse_board('O_XOXX___')
# [-1, 0, 1, -1, 1, 1, 0, 0, 0]
```

### `format_board(board: List[int]) -> str`

Formats a board list into a 3-line display string.

```python
BoardUtils.format_board([-1, 0, 1, -1, 1, 1, 0, 0, 0])
# 'O_X\nOXX\n___'
```

### `get_successors(board: List[int], player: int) -> List[Tuple[int, List[int]]]`

Generates all successor board states for the given player. Returns a list of `(move_index, new_board)` tuples — one for each empty cell.

```python
board = [1, -1, 1, -1, 0, 0, 0, 0, 0]
successors = BoardUtils.get_successors(board, 1)
# [(4, [1, -1, 1, -1, 1, 0, 0, 0, 0]),
#  (5, [1, -1, 1, -1, 0, 1, 0, 0, 0]),
#  ...]
```

### `is_terminal(board: List[int]) -> bool`

Returns `True` if the board is in a terminal state — either a player has won or the board is full.

### `utility(board: List[int]) -> int`

Evaluates a terminal board state. Returns `1` if X wins, `-1` if O wins, `0` for a draw.

### `current_player(board: List[int]) -> int`

Determines whose turn it is based on piece counts. X always moves first. Returns `1` when X/O counts are equal, `-1` otherwise.

```python
BoardUtils.current_player([0, 0, 0, 0, 0, 0, 0, 0, 0])
# 1 (X's turn — empty board, counts equal)

BoardUtils.current_player([1, 0, 0, 0, 0, 0, 0, 0, 0])
# -1 (O's turn — X has 1, O has 0)
```

## Alias

`BoardUtils` is also exported as `Board` from `app.utils`:

```python
from app.utils import Board
Board.parse_board('O_XOXX___')
```
