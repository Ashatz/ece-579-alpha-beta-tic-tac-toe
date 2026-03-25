# Tic-Tac-Toe Events

**Module:** `app/events/tictactoe.py`

Two chained domain events that together implement the solver pipeline. `SolveTicTacToe` handles computation and `PrintResults` handles presentation — cleanly separated via Tiferet's `data_key` mechanism in `feature.yml`.

## SolveTicTacToe

Orchestrates four search algorithm variants and collects results.

### Parameters

- **`board`** (required) — A 9-character string using `X`, `O`, `_`.

### Validation

Uses `self.verify()` to enforce:
- Board must be exactly 9 characters.
- Board must contain only `X`, `O`, or `_`.

Invalid input raises `INVALID_INPUT` (defined in `app/configs/error.yml`).

### Execution Flow

1. Parse the board string via `BoardUtils.parse_board()`.
2. **Minimax** — Run `Minimax.run()` → create a `GameResultAggregate`.
3. **Plain Alpha-Beta** — Create a `GameResultAggregate`, run `AlphaBeta.run()` with `on_cutoff` only.
4. **AB + Killer Heuristic** — Create a `GameResultAggregate`, run `AlphaBeta.run()` with `on_cutoff`, `on_killer`, `get_killers`.
5. **AB + Killer + Transposition** — Create a `GameResultAggregate`, run `AlphaBeta.run()` with all callbacks (cutoff, killer, and transposition).
6. Return a results dict:

```python
{
    'board': List[int],                            # parsed board
    'minimax_result': GameResultAggregate,         # minimax outcome
    'alphabeta_result': GameResultAggregate,       # plain AB with cutoffs
    'killer_result': GameResultAggregate,          # AB + killer heuristic
    'transposition_result': GameResultAggregate,   # AB + killer + transposition
}
```

The feature config stores this dict into request data via `data_key: results`.

### Container Registration

```yaml
# app/configs/container.yml
solve_tictactoe_evt:
  module_path: app.events.tictactoe
  class_name: SolveTicTacToe
```

## PrintResults

Reads the results dict from request data and prints formatted output per homework spec.

### Parameters

- **`results`** (required) — The dict stored by `SolveTicTacToe` via `data_key`.

### Output Format

1. Initial board (3 rows)
2. Minimax results: `Game Result: {value}` + `Moves considered without alpha-beta pruning: {nodes}`
3. For each cutoff in the plain AB result: board (3 rows) + cutoff type, separated by blank lines
4. Plain AB summary: `Game Result: {value}` + `Moves considered with alpha-beta pruning: {nodes}` + `Alpha cuts: {n}` + `Beta cuts: {n}`
5. Killer heuristic summary: `Game Result: {value}` + `Moves considered with killer heuristic: {nodes}` + `Alpha cuts: {n}` + `Beta cuts: {n}`
6. Rotation invariance summary: `Game Result: {value}` + `Moves considered with rotation invariance: {nodes}` + `Transposition hits: {n}` + `Alpha cuts: {n}` + `Beta cuts: {n}`

### Container Registration

```yaml
# app/configs/container.yml
print_results_evt:
  module_path: app.events.tictactoe
  class_name: PrintResults
```

## Feature Chain

The two events are chained in `app/configs/feature.yml`:

```yaml
features:
  tictactoe:
    solve:
      name: Solve Tic-Tac-Toe
      commands:
        - attribute_id: solve_tictactoe_evt
          name: Solve the board with Minimax and Alpha-Beta
          data_key: results
        - attribute_id: print_results_evt
          name: Print formatted results to stdout
```

The `data_key: results` on the first command stores its return value into `request.data['results']`. The second command receives it as the `results` parameter.

## GameResultAggregate

**Module:** `app/mappers/result.py`

The mutable aggregate that bridges the domain and utility layers. Each algorithm variant gets its own aggregate instance. Key members:

- **`record_cutoff(board, cutoff_type)`** — Creates a `Cutoff` domain object and appends to `self.cutoffs`.
- **`record_killer(depth, move)`** — Creates a `KillerMove` domain object and appends to `self.killers`.
- **`get_killers_at_depth(depth)`** — Returns killer move indices at the given depth.
- **`store_transposition(canonical_board, value, depth)`** — Stores an entry in the internal `_transposition_table` dict and appends a `TranspositionEntry` to `self.transpositions`.
- **`lookup_transposition(canonical_board)`** — Returns the stored value or `None`.
- **`increment_transposition_hit()`** — Increments the `_transposition_hits` counter.
- **`alpha_cuts`** (property) — Count of alpha cutoffs.
- **`beta_cuts`** (property) — Count of beta cutoffs.
- **`transposition_hits`** (property) — Number of transposition table hits.

This keeps the aggregate as the single point of mutation — the utility never modifies domain state directly.
