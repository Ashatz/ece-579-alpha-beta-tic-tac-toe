# TicTacToeBoard

**Module:** `app/domain/board.py`

A read-only domain object representing a tic-tac-toe board state.

## Attributes

- **`cells`** — `ListType(IntegerType)`, required. The board as a list of 9 integers (`1` = X, `-1` = O, `0` = empty).
- **`current_player`** — `IntegerType`, required. The player whose turn it is (`1` for X, `-1` for O).

## Usage

```python
from tiferet import DomainObject
from app.domain.board import TicTacToeBoard

board = DomainObject.new(
    TicTacToeBoard,
    cells=[-1, 0, 1, -1, 1, 1, 0, 0, 0],
    current_player=-1,
)

print(board.cells)           # [-1, 0, 1, -1, 1, 1, 0, 0, 0]
print(board.current_player)  # -1
```

## Notes

- This domain object is not currently used in the runtime flow — the solve event works directly with `List[int]` from `BoardUtils.parse_board()`. It exists as a structural definition for the board concept and can be used in future extensions (e.g., persisting game state, passing typed objects between events).
- As a `DomainObject`, it is read-only. If mutation is needed, define an aggregate in `app/mappers/`.
