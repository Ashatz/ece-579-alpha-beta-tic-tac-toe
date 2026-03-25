# Cutoff, KillerMove, TranspositionEntry & GameResult

**Module:** `app/domain/result.py`

Four domain objects sharing the same module — all are part of the result bounded context.

## Cutoff

A read-only domain object representing a single alpha-beta pruning event.

### Attributes

- **`board`** — `ListType(IntegerType)`, required. The board state at the node where pruning occurred.
- **`cutoff_type`** — `StringType`, required. Either `'Alpha cut'` or `'Beta cut'`.

### Usage

```python
from tiferet import DomainObject
from app.domain.result import Cutoff

cutoff = DomainObject.new(
    Cutoff,
    board=[-1, -1, 1, -1, 1, 1, 0, 1, 0],
    cutoff_type='Alpha cut',
)
```

Cutoffs are not created directly in application code. Instead, `GameResultAggregate.record_cutoff()` creates them during alpha-beta search.

## KillerMove

A read-only domain object representing a killer move recorded during alpha-beta search. A killer move is one that caused a cutoff at a particular depth — used for move ordering on subsequent branches.

### Attributes

- **`depth`** — `IntegerType`, required. The search depth where the cutoff occurred.
- **`move`** — `IntegerType`, required. The move index (0–8) that caused the cutoff.

### Usage

```python
from tiferet import DomainObject
from app.domain.result import KillerMove

killer = DomainObject.new(KillerMove, depth=2, move=4)
```

KillerMoves are created by `GameResultAggregate.record_killer()` during alpha-beta search.

## TranspositionEntry

A read-only domain object representing an entry in the rotation-invariant transposition table. Stores the evaluated value for a canonical board position.

### Attributes

- **`canonical_board`** — `ListType(IntegerType)`, required. The canonical (lexicographically smallest rotation) board key.
- **`value`** — `IntegerType`, required. The evaluated minimax value.
- **`depth`** — `IntegerType`, required. The search depth at which this was evaluated.

### Usage

```python
from tiferet import DomainObject
from app.domain.result import TranspositionEntry

entry = DomainObject.new(
    TranspositionEntry,
    canonical_board=[0, 0, 0, -1, 0, 0, 1, 0, 0],
    value=0,
    depth=1,
)
```

TranspositionEntries are created by `GameResultAggregate.store_transposition()` during alpha-beta search.

## GameResult

A read-only domain object representing the result of a game search algorithm.

### Attributes

- **`value`** — `IntegerType`, required. The utility value (`1` = X wins, `-1` = O wins, `0` = draw).
- **`nodes`** — `IntegerType`, required. Total nodes evaluated during search.
- **`algorithm`** — `StringType`, required. Algorithm identifier (e.g., `'minimax'`, `'alphabeta'`, `'alphabeta_killer'`, `'alphabeta_killer_trans'`).
- **`cutoffs`** — `ListType(ModelType(Cutoff))`, default `[]`. List of pruning events.
- **`killers`** — `ListType(ModelType(KillerMove))`, default `[]`. List of killer moves recorded.
- **`transpositions`** — `ListType(ModelType(TranspositionEntry))`, default `[]`. List of transposition table entries stored.

### Usage

```python
from tiferet import DomainObject
from app.domain.result import GameResult

result = DomainObject.new(
    GameResult,
    value=-1,
    nodes=26,
    algorithm='minimax',
)

print(result.value)          # -1
print(result.cutoffs)        # []
print(result.killers)        # []
print(result.transpositions) # []
```

## GameResultAggregate

**Module:** `app/mappers/result.py`

Mutable aggregate extending `GameResult` with cutoff collection.

### Methods

- **`record_cutoff(board: List[int], cutoff_type: str)`** — Creates a `Cutoff` via `DomainObject.new()` and appends it to `self.cutoffs`. This method is passed as the `on_cutoff` callback into `AlphaBeta.run()`.

### Properties

- **`alpha_cuts`** — Count of cutoffs where `cutoff_type == 'Alpha cut'`.
- **`beta_cuts`** — Count of cutoffs where `cutoff_type == 'Beta cut'`.

### Usage

```python
from tiferet import Aggregate
from app.mappers.result import GameResultAggregate

aggregate = Aggregate.new(
    GameResultAggregate,
    value=0,
    nodes=0,
    algorithm='alphabeta',
    cutoffs=[],
    validate=False,
)

# Pass record_cutoff as the on_cutoff callback to AlphaBeta
from app.utils.alphabeta import AlphaBeta
from app.utils.board_utils import BoardUtils

board = BoardUtils.parse_board('O_XOXX___')
value, nodes = AlphaBeta.run(board, on_cutoff=aggregate.record_cutoff)

aggregate.set_attribute('value', value)
aggregate.set_attribute('nodes', nodes)

print(aggregate.alpha_cuts)  # 1
print(aggregate.beta_cuts)   # 4
print(len(aggregate.cutoffs))  # 5
```
