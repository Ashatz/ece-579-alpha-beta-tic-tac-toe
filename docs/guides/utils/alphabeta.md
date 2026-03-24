# AlphaBeta

**Module:** `app/utils/alphabeta.py`

Alpha-beta pruning search. All methods are static — pure computation with no side effects. Cutoff events are reported via an optional callback rather than printing directly.

## Methods

### `search(board, alpha, beta, is_maximizing, on_cutoff=None) -> Tuple[int, int]`

Runs alpha-beta pruning search from the given board state.

- **`board`** — Current board state as `List[int]`.
- **`alpha`** / **`beta`** — Current bounds as `float`.
- **`is_maximizing`** — `True` if the current player is X (maximizer).
- **`on_cutoff`** — Optional callable invoked as `on_cutoff(board, cutoff_type)` when pruning occurs. `board` is the parent board state at the point of cutoff. `cutoff_type` is `'Alpha cut'` or `'Beta cut'`.
- **Returns** — `(utility_value, node_count)`.

**Cutoff semantics:**
- **Beta cutoff** (maximizing node): `alpha >= beta` — the maximizer found a value that exceeds the minimizer's best option, so remaining branches are pruned.
- **Alpha cutoff** (minimizing node): `beta <= alpha` — the minimizer found a value below the maximizer's best option.

```python
from app.utils.board_utils import BoardUtils
from app.utils.alphabeta import AlphaBeta

board = BoardUtils.parse_board('O_XOXX___')
cutoffs = []
value, nodes = AlphaBeta.search(
    board, float('-inf'), float('inf'), False,
    on_cutoff=lambda b, t: cutoffs.append((b, t))
)
# value = -1, nodes = 17, cutoffs has 5 entries
```

### `run(board: List[int], on_cutoff=None) -> Tuple[int, int]`

Convenience wrapper that auto-detects whose turn it is and initializes alpha/beta to `±inf`.

```python
value, nodes = AlphaBeta.run(
    BoardUtils.parse_board('O_XOXX___'),
    on_cutoff=lambda b, t: print(f'{t} at {b}')
)
```

## The `on_cutoff` Callback

The callback is the key design feature that keeps this utility side-effect-free. In the full application, `GameResultAggregate.record_cutoff` is passed as the callback — the aggregate creates `Cutoff` domain objects and collects them for later formatting by the `PrintResults` event.

The callback signature is:

```python
def on_cutoff(board: List[int], cutoff_type: str) -> None
```

- **`board`** — The board state at the node where pruning occurred (the parent, not the child that triggered it).
- **`cutoff_type`** — Either `'Alpha cut'` or `'Beta cut'`.
