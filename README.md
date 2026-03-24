# Tic-Tac-Toe Solver — Minimax & Alpha-Beta Pruning

**ECE 479/579 Homework 4** · Built with [Tiferet](https://github.com/greatstrength/tiferet) v2.0

A clean, domain-driven Tic-Tac-Toe solver that compares plain Minimax search against Alpha-Beta pruning. The solver reports the game result, total nodes evaluated by each algorithm, and every pruning cutoff with its board state — demonstrating the efficiency gains of Alpha-Beta over exhaustive Minimax.

## Quick Start

```bash
# Clone and set up
git clone https://github.com/Ashatz/ece-579-alpha-beta-tic-tac-toe.git
cd ece-579-alpha-beta-tic-tac-toe
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# Solve a board
python tictactoe_cli.py tictactoe solve O_XOXX___
```

## Board Format

Boards are 9-character strings read left-to-right, top-to-bottom:

- `X` — X player
- `O` — O player
- `_` — empty cell

For example, `O_XOXX___` represents:

```
O_X
OXX
___
```

## Example Output

```
$ python tictactoe_cli.py tictactoe solve O_XOXX___
O_X
OXX
___
Game Result: -1
Moves considered without alpha-beta pruning: 26
OOX
OXX
_X_
Alpha cut

OXX
OXX
_OO
Beta cut

...

Game Result: -1
Moves considered with alpha-beta pruning: 17
Alpha cuts: 1
Beta cuts: 4
```

- **Game Result**: `1` = X wins, `-1` = O wins, `0` = draw
- **Moves considered**: Total nodes evaluated during search
- **Cutoff blocks**: Each shows the board state where pruning occurred, followed by the cut type

## Architecture

The project follows a Domain-Driven Design (DDD) architecture using the Tiferet framework:

```
app/
├── configs/            # Tiferet YAML configurations
│   ├── app.yml         # Interface definitions
│   ├── cli.yml         # CLI command structure
│   ├── container.yml   # Dependency injection
│   ├── error.yml       # Error definitions (INVALID_INPUT)
│   ├── feature.yml     # Feature workflow (chained events)
│   └── logging.yml     # Logging configuration
├── domain/             # Read-only domain objects
│   ├── board.py        # TicTacToeBoard
│   └── result.py       # Cutoff + GameResult (same bounded context)
├── events/             # Domain events (business logic)
│   └── tictactoe.py    # SolveTicTacToe + PrintResults
├── mappers/            # Aggregates (mutable domain extensions)
│   └── result.py       # GameResultAggregate — collects cutoffs
└── utils/              # Utility classes with static methods (no I/O)
    ├── board_utils.py  # BoardUtils — parsing, formatting, game logic
    ├── minimax.py      # Minimax — plain recursive search
    └── alphabeta.py    # AlphaBeta — search with callback-based cutoff capture
```

### Design Highlights

- **Utils are side-effect-free classes**: `AlphaBeta.search()` accepts an optional `on_cutoff` callable instead of printing directly. All utility methods are static — no I/O in the computation layer.
- **Aggregate root pattern**: `GameResultAggregate` owns the cutoff list and provides `record_cutoff()` as the callback injected into the Alpha-Beta utility. Cutoff counts are derived properties.
- **Chained domain events**: The feature workflow chains `SolveTicTacToe` (computation, stores results via `data_key`) → `PrintResults` (reads results, formats output). Clean separation of computation from presentation.
- **Tiferet CLI integration**: The CLI is wired entirely through YAML configs — command parsing, feature routing, and dependency injection are handled by the framework.

## Development

### Prerequisites

- Python ≥ 3.10
- Tiferet 2.0.0a6

### Running

```bash
python tictactoe_cli.py tictactoe solve <9-character-board>
```

### Project Conventions

All source files follow the Tiferet structured code style:

- Artifact comments (`# ***`, `# **`, `# *`) for hierarchical organization
- RST-format docstrings with `:param`, `:type`, `:return`, `:rtype`
- Logical code snippets separated by intent comments

See `AGENTS.md` for detailed contributor and AI agent guidance.

### Guides

- **Utils:** [BoardUtils](docs/guides/utils/board_utils.md) · [Minimax](docs/guides/utils/minimax.md) · [AlphaBeta](docs/guides/utils/alphabeta.md)
- **Domain:** [TicTacToeBoard](docs/guides/domain/board.md) · [Cutoff & GameResult](docs/guides/domain/result.md)
- **Events:** [SolveTicTacToe & PrintResults](docs/guides/events/tictactoe.md)

## License

See [LICENSE](LICENSE) for details.
