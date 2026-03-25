# AlphaBeta

**Module:** `app/utils/alphabeta.py`

Alpha-beta pruning search with optional killer heuristic and rotation-invariant transposition table support. All methods are static — pure computation with no side effects. All state interaction occurs through optional callbacks.

## Methods

### `search(board, alpha, beta, is_maximizing, depth, on_cutoff, on_killer, get_killers, lookup_transposition, store_transposition, on_transposition_hit) -> Tuple[int, int]`

Runs alpha-beta pruning search from the given board state.

- **`board`** — Current board state as `List[int]`.
- **`alpha`** / **`beta`** — Current bounds as `float`.
- **`is_maximizing`** — `True` if the current player is X (maximizer).
- **`depth`** — Current search depth (0 at root). Used for killer move tracking.
- **`on_cutoff`** — Optional. Invoked as `on_cutoff(board, cutoff_type)` when pruning occurs.
- **`on_killer`** — Optional. Invoked as `on_killer(depth, move)` when a cutoff-causing move is found.
- **`get_killers`** — Optional. Invoked as `get_killers(depth) -> List[int]` to retrieve killer moves for move ordering.
- **`lookup_transposition`** — Optional. Invoked as `lookup_transposition(canonical_board) -> int | None` before expanding a node.
- **`store_transposition`** — Optional. Invoked as `store_transposition(canonical_board, value, depth)` after fully exploring a node.
- **`on_transposition_hit`** — Optional. Invoked (no args) when a transposition table hit occurs.
- **Returns** — `(utility_value, node_count)`.

All callback parameters default to `None` and are fully backward-compatible — plain alpha-beta works with just `on_cutoff`.

**Cutoff semantics:**
- **Beta cutoff** (maximizing node): `alpha >= beta` — the maximizer found a value that exceeds the minimizer's best option, so remaining branches are pruned.
- **Alpha cutoff** (minimizing node): `beta <= alpha` — the minimizer found a value below the maximizer's best option.

```python
from app.utils.board_utils import BoardUtils
from app.utils.alphabeta import AlphaBeta

# Plain alpha-beta (backward compatible)
board = BoardUtils.parse_board('O_XOXX___')
cutoffs = []
value, nodes = AlphaBeta.search(
    board, float('-inf'), float('inf'), False,
    on_cutoff=lambda b, t: cutoffs.append((b, t))
)
# value = -1, nodes = 17, cutoffs has 5 entries
```

### `run(board, on_cutoff, on_killer, get_killers, lookup_transposition, store_transposition, on_transposition_hit) -> Tuple[int, int]`

Convenience wrapper that auto-detects whose turn it is, initializes alpha/beta to `±inf` and depth to `0`.

```python
# Plain alpha-beta
value, nodes = AlphaBeta.run(board, on_cutoff=aggregate.record_cutoff)

# With killer heuristic
value, nodes = AlphaBeta.run(board,
    on_cutoff=aggregate.record_cutoff,
    on_killer=aggregate.record_killer,
    get_killers=aggregate.get_killers_at_depth,
)

# With killer heuristic + transposition table
value, nodes = AlphaBeta.run(board,
    on_cutoff=aggregate.record_cutoff,
    on_killer=aggregate.record_killer,
    get_killers=aggregate.get_killers_at_depth,
    lookup_transposition=aggregate.lookup_transposition,
    store_transposition=aggregate.store_transposition,
    on_transposition_hit=aggregate.increment_transposition_hit,
)
```

### `_reorder_successors(successors, killer_moves) -> List[Tuple[int, List[int]]]`

Private static method. Reorders successors so killer moves are tried first. Used internally by `search()` when `get_killers` is provided.

## Callbacks

Callbacks are the key design feature that keeps this utility side-effect-free. In the full application, `GameResultAggregate` methods are passed as callbacks — the aggregate manages all mutable state.

### `on_cutoff(board: List[int], cutoff_type: str) -> None`

Invoked when a pruning event occurs. `board` is the parent board state at the point of cutoff. `cutoff_type` is `'Alpha cut'` or `'Beta cut'`.

### `on_killer(depth: int, move: int) -> None`

Invoked when a move causes a cutoff. Records the move as a "killer" at the given depth for future move ordering.

### `get_killers(depth: int) -> List[int]`

Returns a list of killer move indices recorded at the given depth. Used to reorder successors via `_reorder_successors()`.

### `lookup_transposition(canonical_board: Tuple[int, ...]) -> int | None`

Looks up a canonical board position in the transposition table. Returns the stored value if found, `None` otherwise. The canonical board key is computed via `BoardUtils.get_canonical_board()`.

### `store_transposition(canonical_board: Tuple[int, ...], value: int, depth: int) -> None`

Stores an evaluated position in the transposition table. **Only called when no cutoff occurred at the current node** (exact values only), ensuring correctness.

### `on_transposition_hit() -> None`

Invoked when a transposition table lookup succeeds, for hit counting.

## Killer Heuristic

The killer heuristic improves move ordering by recording which moves caused cutoffs at each depth. When exploring a new node at depth `d`, the search first checks if any killer moves exist for that depth (via `get_killers(d)`). If so, those moves are tried before other successors.

This works because moves that cause cutoffs in one branch often cause cutoffs in sibling branches at the same depth. Better move ordering means earlier cutoffs, which means fewer nodes explored.

## Transposition Table

The transposition table avoids re-evaluating board positions that have already been fully explored. Before expanding any node, the search computes the canonical board key (via `BoardUtils.get_canonical_board()`) and checks the table. If a hit is found, the stored value is returned immediately.

**Correctness guarantee:** Only exact values are stored — if a cutoff occurred at the current node, the value is a bound (not exact) and is not stored. This prevents incorrect reuse of partial evaluations.

**Rotation invariance:** The canonical key is the lexicographically smallest of all four rotations (0°, 90°, 180°, 270°), so rotated positions are recognized as equivalent.

## Performance

Results from the empty board (`_________`) — the worst case for tic-tac-toe:

- **Minimax:** 549,946 nodes (baseline)
- **Alpha-Beta:** 18,297 nodes (96.7% reduction)
- **AB + Killer:** 15,681 nodes (further 14.3% reduction)
- **AB + Killer + Transposition:** 3,239 nodes (further 79.3% reduction, 728 transposition hits)
