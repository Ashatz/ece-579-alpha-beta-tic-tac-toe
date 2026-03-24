# Tic-Tac-Toe Events

**Module:** `app/events/tictactoe.py`

Two chained domain events that together implement the solver pipeline. `SolveTicTacToe` handles computation and `PrintResults` handles presentation — cleanly separated via Tiferet's `data_key` mechanism in `feature.yml`.

## SolveTicTacToe

Orchestrates both search algorithms and collects results.

### Parameters

- **`board`** (required) — A 9-character string using `X`, `O`, `_`.

### Validation

Uses `self.verify()` to enforce:
- Board must be exactly 9 characters.
- Board must contain only `X`, `O`, or `_`.

Invalid input raises `INVALID_INPUT` (defined in `app/configs/error.yml`).

### Execution Flow

1. Parse the board string via `BoardUtils.parse_board()`.
2. Run `Minimax.run()` → create a `GameResultAggregate` with the minimax results.
3. Create a second `GameResultAggregate` for alpha-beta (with placeholder values).
4. Run `AlphaBeta.run()`, passing `aggregate.record_cutoff` as the `on_cutoff` callback. The aggregate collects `Cutoff` domain objects during the search.
5. Update the alpha-beta aggregate with final `value` and `nodes` via `set_attribute()`.
6. Return a results dict:

```python
{
    'board': List[int],                      # parsed board
    'minimax_result': GameResultAggregate,   # minimax outcome
    'alphabeta_result': GameResultAggregate, # alphabeta outcome with cutoffs
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
3. For each cutoff in the alphabeta result: board (3 rows) + cutoff type, separated by blank lines
4. Alpha-beta summary: `Game Result: {value}` + `Moves considered with alpha-beta pruning: {nodes}` + `Alpha cuts: {n}` + `Beta cuts: {n}`

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

The mutable aggregate that bridges the domain and utility layers. Key members:

- **`record_cutoff(board, cutoff_type)`** — Creates a `Cutoff` domain object and appends it to `self.cutoffs`. This method is passed as the `on_cutoff` callback into `AlphaBeta.run()`.
- **`alpha_cuts`** (property) — Count of cutoffs where `cutoff_type == 'Alpha cut'`.
- **`beta_cuts`** (property) — Count of cutoffs where `cutoff_type == 'Beta cut'`.

This keeps the aggregate as the single point of mutation — the utility never modifies domain state directly.
