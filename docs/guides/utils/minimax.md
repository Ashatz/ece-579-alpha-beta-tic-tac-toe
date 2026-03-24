# Minimax

**Module:** `app/utils/minimax.py`

Plain recursive minimax search. All methods are static — no pruning, no callbacks, no side effects.

## Methods

### `search(board: List[int], is_maximizing: bool) -> Tuple[int, int]`

Runs a full minimax search from the given board state. Every node in the game tree is explored — no pruning.

- **`board`** — Current board state as `List[int]`.
- **`is_maximizing`** — `True` if the current player is X (maximizer), `False` for O (minimizer).
- **Returns** — `(utility_value, node_count)` where `node_count` includes every recursive call (internal nodes + terminals).

```python
from app.utils.board_utils import BoardUtils
from app.utils.minimax import Minimax

board = BoardUtils.parse_board('O_XOXX___')
value, nodes = Minimax.search(board, is_maximizing=False)
# value = -1 (O wins), nodes = 26
```

### `run(board: List[int]) -> Tuple[int, int]`

Convenience wrapper that auto-detects whose turn it is via `BoardUtils.current_player()` and calls `search()`.

```python
value, nodes = Minimax.run(BoardUtils.parse_board('O_XOXX___'))
# value = -1, nodes = 26
```

## Node Counting

Every call to `search()` counts as one node — both internal (non-terminal) nodes and leaf (terminal) nodes. The total is the sum across the entire recursion tree. This matches the "moves considered" metric in the output.
