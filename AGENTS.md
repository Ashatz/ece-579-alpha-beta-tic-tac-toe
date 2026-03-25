# AGENTS.md — Tic-Tac-Toe Solver (v0.2.0)

## Project Overview

A Tic-Tac-Toe solver comparing plain Minimax against Alpha-Beta pruning **with Killer Heuristic and Rotation Invariance**, built with the Tiferet DDD framework. The solver accepts a 9-character board string, runs four algorithm variants, captures pruning events as domain objects, and prints formatted results via a chained domain event pipeline.

- **Repository:** https://github.com/Ashatz/ece-579-alpha-beta-tic-tac-toe
- **Branch:** `v0.2-release`
- **Python:** ≥ 3.10
- **Framework:** Tiferet 2.0.0a6

## Architecture

### Layer Overview

```
app/
├── configs/            # Tiferet YAML wiring
├── domain/             # Read-only domain objects (DomainObject)
├── events/tictactoe.py # Domain events (DomainEvent)
├── mappers/            # Aggregates (mutable domain extensions)
└── utils/              # Pure computational utilities (no I/O, no framework)
```

### Key Design Decisions

**Side-effect-free utility classes.** `AlphaBeta.search()` accepts optional callbacks (`on_cutoff`, `on_killer`, `get_killers`, `lookup_transposition`, `store_transposition`, `on_transposition_hit`) instead of managing state directly. `Minimax.search()` is purely recursive. All utility methods are static — no I/O, no global state, no dependency on the domain layer.

**Cutoff as a domain object.** Each Alpha-Beta pruning event is captured as a `Cutoff(DomainObject)` with the board state and cut type. This keeps pruning data first-class and inspectable rather than ephemeral print output.

**Killer Heuristic via callbacks.** The Killer Heuristic records cutoff-causing moves at each depth (`on_killer` callback) and uses them for improved move ordering (`get_killers` callback). Successors are reordered to try killer moves first, typically reducing nodes explored by 10–15% vs plain alpha-beta.

**Rotation Invariance via Transposition Table.** A transposition table stores evaluation results using a rotation-invariant canonical board representation. `BoardUtils.get_canonical_board()` generates all four rotations (0°, 90°, 180°, 270°) and returns the lexicographically smallest as a hashable tuple key. Only **exact values** (fully explored nodes with no cutoff) are stored to guarantee correctness.

**Aggregate root for mutation.** `GameResultAggregate` extends `GameResult` with mutation methods for cutoffs, killers, and transpositions. It manages an internal `_transposition_table` dict for O(1) lookups and a `_transposition_hits` counter. Aggregate methods are passed directly as callbacks into the Alpha-Beta utility, keeping the aggregate as the single point of mutation.

**Four-algorithm comparison.** The feature `tictactoe.solve` chains two events. `SolveTicTacToe` runs four algorithm variants (Minimax, plain AB, AB+Killer, AB+Killer+Transposition) and `PrintResults` displays the progression, demonstrating the incremental benefit of each optimization.

**Chained domain events.** The feature `tictactoe.solve` chains two events via `feature.yml`:
1. `SolveTicTacToe` — validates input, runs all four algorithms, stores results dict via `data_key: results`
2. `PrintResults` — reads results from request data, formats and prints per spec

This separates computation from presentation cleanly.

### Runtime Flow

1. `tictactoe_cli.py` → `App().load_interface('tictactoe_cli')` → `CliContext`
2. CLI parses `tictactoe solve <board>` → routes to feature `tictactoe.solve`
3. `SolveTicTacToe.execute(board)`:
   - Validates board string (length 9, chars in {X, O, _})
   - Parses board → runs `Minimax.run()` → creates minimax `GameResultAggregate`
   - Runs plain `AlphaBeta.run()` with `on_cutoff` only → creates AB result
   - Runs `AlphaBeta.run()` with `on_cutoff`, `on_killer`, `get_killers` → creates killer result
   - Runs `AlphaBeta.run()` with all callbacks (killer + transposition) → creates transposition result
   - Returns `{board, minimax_result, alphabeta_result, killer_result, transposition_result}` → stored to request data via `data_key`
4. `PrintResults.execute(results)`:
   - Reads results dict → prints initial board, minimax stats, cutoff blocks, plain AB stats, killer stats, transposition stats

## Structured Code Style

All code follows the Tiferet artifact comment hierarchy. This is mandatory for all new code.

### Comment Levels

- `# *** <section>` — Top-level: `imports`, `constants`, `utils`, `models`, `events`, `mappers`
- `# ** <category>: <name>` — Mid-level: `core`/`infra`/`app` (imports); `util: <name>`, `model: <name>`, `event: <name>`, `mapper: <name>`
- `# * <component>` — Low-level: `attribute: <name>`, `init`, `method: <name>`, `method: <name> (static)`, `property: <name>`

### Spacing Rules

- One empty line between `# ***` and first `# **`
- One empty line between each `# *` section
- One empty line after docstrings and between code snippets within methods

### Docstrings

RST format with `:param`, `:type`, `:return`, `:rtype` for all public functions and methods.

### Code Snippets

Each logical step within a method is a separate snippet preceded by a 1–2 line comment:

```python
# Parse the board string into a list of integers.
cells = BoardUtils.parse_board(board)

# Run plain minimax search.
mm_value, mm_nodes = Minimax.run(cells)
```

## Component Reference

### Utils (`app/utils/`)

Utility classes with static methods. No framework dependencies. Testable in isolation.

- **`board_utils.py`** — `BoardUtils` with static methods: `parse_board`, `format_board`, `get_successors`, `is_terminal`, `utility`, `current_player`, `rotate_90`, `rotate_180`, `rotate_270`, `get_canonical_board`
- **`minimax.py`** — `Minimax` with static methods: `search(board, is_maximizing)` → `(value, node_count)`, `run(board)` convenience wrapper
- **`alphabeta.py`** — `AlphaBeta` with static methods: `_reorder_successors(successors, killer_moves)` (private), `search(board, alpha, beta, is_maximizing, depth, on_cutoff, on_killer, get_killers, lookup_transposition, store_transposition, on_transposition_hit)` → `(value, node_count)`, `run(board, ...)` convenience wrapper

### Domain Objects (`app/domain/`)

Read-only. Extend `DomainObject` from Tiferet. Instantiate via `DomainObject.new(Type, **kwargs)`.

- **`board.py`** — `TicTacToeBoard` with `cells: ListType(IntegerType)`, `current_player: IntegerType`
- **`result.py`** — `Cutoff` with `board`, `cutoff_type`; `KillerMove` with `depth`, `move`; `TranspositionEntry` with `canonical_board`, `value`, `depth`; `GameResult` with `value`, `nodes`, `algorithm`, `cutoffs`, `killers`, `transpositions`. All are in the same module — part of the result bounded context.

### Mappers (`app/mappers/`)

Mutable extensions of domain objects. Extend both the domain object and `Aggregate`.

- **`GameResultAggregate`** — Adds `record_cutoff(board, cutoff_type)`, `record_killer(depth, move)`, `get_killers_at_depth(depth)`, `store_transposition(canonical_board, value, depth)`, `lookup_transposition(canonical_board)`, `increment_transposition_hit()`, properties `alpha_cuts`, `beta_cuts`, `transposition_hits`. Internal `_transposition_table` dict and `_transposition_hits` counter.

### Domain Events (`app/events/tictactoe.py`)

Both events live in a single module. Extend `DomainEvent`. Use `@DomainEvent.parameters_required([...])` for input validation and `self.verify()` for domain rules.

- **`SolveTicTacToe`** — Orchestrates four algorithm variants (minimax, plain AB, AB+killer, AB+killer+transposition), returns results dict
- **`PrintResults`** — Formats and prints output per homework spec, showing the progression across all four variants

### Configs (`app/configs/`)

- **`app.yml`** — Defines `basic_tictactoe` (default) and `tictactoe_cli` (CliContext) interfaces
- **`cli.yml`** — CLI command `tictactoe solve <board>`
- **`container.yml`** — Registers `solve_tictactoe_evt` and `print_results_evt`
- **`error.yml`** — Defines `INVALID_INPUT` error with localized message
- **`feature.yml`** — Chains the two events with `data_key` for data passing
- **`logging.yml`** — Minimal logging (WARNING level, suppresses framework noise)

## Board Representation

- **String format** (CLI input): `X`, `O`, `_` — 9 characters, left-to-right top-to-bottom
- **Internal format** (utils/domain): `List[int]` — `1` = X, `-1` = O, `0` = empty
- **Conversion**: `BoardUtils.parse_board()` (string → list), `BoardUtils.format_board()` (list → display string)
- **Player detection**: X moves first; `BoardUtils.current_player()` returns `1` when X/O counts are equal, `-1` otherwise
- **Canonical form**: `BoardUtils.get_canonical_board()` returns the lexicographically smallest of all four rotations as a `Tuple[int, ...]` for use as a hashable transposition table key

## Extending the Project

### Adding a new algorithm

1. Create `app/utils/new_algo.py` with a utility class matching the pattern: static `search()` method + static `run()` convenience wrapper returning `(value, node_count)`
2. Wire it into `SolveTicTacToe.execute()` — create a `GameResultAggregate`, pass aggregate methods as callbacks
3. Update `PrintResults.execute()` to format the new results

### Adding a new domain event

1. Create the event class in `app/events/tictactoe.py` (or a new module under `app/events/`)
2. Register it in `app/configs/container.yml` with an `_evt` suffix
3. Add it to the feature chain in `app/configs/feature.yml`

### Testing

- Utils can be tested in isolation with plain `pytest` — no framework needed
- Domain events should be tested via `DomainEvent.handle(EventClass, dependencies={...}, **kwargs)`
- Mock `GameResultAggregate` when testing events that depend on it

## Conventions Summary

- Container attribute IDs use `_evt` suffix (e.g., `solve_tictactoe_evt`)
- Utils are pure computation — no I/O, no framework imports
- Domain objects are read-only — mutation goes through Aggregates
- Transposition table only stores exact values (no cutoff at current node) for correctness
- All files use the Tiferet artifact comment hierarchy
- Commits include `Co-Authored-By: Oz <oz-agent@warp.dev>` when AI-assisted
