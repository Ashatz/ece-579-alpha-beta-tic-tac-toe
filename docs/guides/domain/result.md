# Cutoff & GameResult

**Module:** `app/domain/result.py`

Two domain objects sharing the same module — both are part of the result bounded context.

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

## GameResult

A read-only domain object representing the result of a game search algorithm.

### Attributes

- **`value`** — `IntegerType`, required. The utility value (`1` = X wins, `-1` = O wins, `0` = draw).
- **`nodes`** — `IntegerType`, required. Total nodes evaluated during search.
- **`algorithm`** — `StringType`, required. Either `'minimax'` or `'alphabeta'`.
- **`cutoffs`** — `ListType(ModelType(Cutoff))`, default `[]`. List of pruning events (empty for minimax results).

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

print(result.value)     # -1
print(result.cutoffs)   # []
```

### Aggregate Extension

`GameResult` is extended by `GameResultAggregate` in `app/mappers/result.py`, which adds mutation methods (`record_cutoff`) and derived properties (`alpha_cuts`, `beta_cuts`). See `docs/guides/events/tictactoe.md` for the full runtime flow.
