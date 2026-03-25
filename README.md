# Tic-Tac-Toe Solver — Minimax, Alpha-Beta, Killer Heuristic & Rotation Invariance

**ECE 479/579 Homework 4** · Built with [Tiferet](https://github.com/greatstrength/tiferet) v2.0

A clean, domain-driven Tic-Tac-Toe solver that compares four search strategies: plain Minimax, Alpha-Beta pruning, Alpha-Beta with Killer Heuristic, and Alpha-Beta with Killer Heuristic + Rotation-Invariant Transposition Table. The solver reports the game result, total nodes evaluated by each variant, pruning cutoffs, transposition hits, and alpha/beta cut counts — demonstrating the incremental efficiency gains of each optimization.

## Submission Information

- **Programming language:** Python 3.10+
- **Development environment:** Visual Studio Code and [Warp](https://www.warp.dev/) (AI-powered terminal)
- **How to compile and run:** See [Quick Start](#quick-start) below. Python is an interpreted language — no compilation step is required.

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
Running without alpha-beta pruning
Game Result: -1
Moves considered without alpha-beta pruning: 26
-----------------------------------------
Running with alpha-beta pruning
OOX
OXX
_X_
Alpha cut

OXX
OXX
_OO
Beta cut

O_X
OXX
_O_
Beta cut

OXX
OXX
_OO
Beta cut

O_X
OXX
__O
Beta cut
Game Result: -1
Moves considered with alpha-beta pruning: 17
Alpha cuts: 1
Beta cuts: 4
-----------------------------------------
Running with the killer heuristic
OOX
OXX
_X_
Alpha cut

OXX
OXX
_OO
Beta cut

O_X
OXX
_O_
Beta cut

OXX
OXX
_OO
Beta cut

O_X
OXX
__O
Beta cut
Game Result: -1
Moves considered with alpha-beta pruning: 17
Alpha cuts: 1
Beta cuts: 4
-----------------------------------------
Running with the killer heuristic and using rotation invariance.
OOX
OXX
_X_
Alpha cut

OXX
OXX
_OO
Beta cut

O_X
OXX
_O_
Beta cut

OXX
OXX
_OO
Beta cut

O_X
OXX
__O
Beta cut
Game Result: -1
Moves considered with alpha-beta pruning: 17
Alpha cuts: 1
Beta cuts: 4
Rotation invariance invoked: 0
```

- **Game Result**: `1` = X wins, `-1` = O wins, `0` = draw
- **Moves considered**: Total nodes evaluated during search
- **Cutoff blocks**: Each shows the board state where pruning occurred, followed by the cut type
- **Rotation invariance invoked**: Number of positions found in the rotation-invariant transposition table

### Performance (Empty Board)

The empty board (`_________`) is the worst case for tic-tac-toe search:

- **Minimax:** 549,946 nodes (baseline)
- **Alpha-Beta:** 18,297 nodes (96.7% reduction)
- **AB + Killer:** 15,681 nodes (further 14.3% reduction)
- **AB + Killer + Transposition:** 3,239 nodes (further 79.3% reduction, 728 transposition hits)

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
│   └── result.py       # Cutoff, KillerMove, TranspositionEntry, GameResult
├── events/             # Domain events (business logic)
│   └── tictactoe.py    # SolveTicTacToe + PrintResults
├── mappers/            # Aggregates (mutable domain extensions)
│   └── result.py       # GameResultAggregate — collects cutoffs, killers, transpositions
└── utils/              # Utility classes with static methods (no I/O)
    ├── board_utils.py  # BoardUtils — parsing, formatting, game logic, rotations
    ├── minimax.py      # Minimax — plain recursive search
    └── alphabeta.py    # AlphaBeta — search with callback-based state interaction
```

### Design Highlights

- **Utils are side-effect-free classes**: `AlphaBeta.search()` accepts optional callbacks (`on_cutoff`, `on_killer`, `get_killers`, transposition callbacks) instead of managing state directly. All utility methods are static — no I/O in the computation layer.
- **Aggregate root pattern**: `GameResultAggregate` owns cutoffs, killers, and transpositions. Aggregate methods are passed as callbacks into the Alpha-Beta utility, keeping it as the single point of mutation.
- **Killer Heuristic**: Records cutoff-causing moves at each depth and reorders successors to try killer moves first.
- **Rotation-Invariant Transposition Table**: Stores evaluation results using the lexicographically smallest board rotation as a canonical key. Only exact values (no cutoffs) are stored for correctness.
- **Four-algorithm comparison**: `SolveTicTacToe` runs Minimax, plain AB, AB+Killer, and AB+Killer+Transposition to demonstrate incremental gains.
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
- **Domain:** [TicTacToeBoard](docs/guides/domain/board.md) · [Cutoff, KillerMove, TranspositionEntry & GameResult](docs/guides/domain/result.md)
- **Events:** [SolveTicTacToe & PrintResults](docs/guides/events/tictactoe.md)

## AI Attribution

This project was developed with assistance from two AI agents:

**Grok** (xAI), was responsible for:
- Providing high-level architectural guidance
- Helping draft the AGENTS.md documents for v0.1.0 and v0.2.0
- Designing the overall structure for Killer Heuristic and Rotation-Invariant Transposition Table integration
- Collaborating on maintaining clean Tiferet DDD patterns and ECE 479/579 course alignment

**Oz** (Claude, Anthropic), running within the [Warp](https://www.warp.dev/) terminal, was responsible for:
- Drafting Technical Requirements Documents (TRDs) for all v0.1.0 and v0.2.0 stories
- Implementing all source code, domain objects, mappers, utilities, events, and configuration
- Writing all documentation (guides, README, AGENTS.md)
- Verifying acceptance criteria and backward compatibility for each story
- Creating pull requests with structured commit messages
- Submitting collaboration reports on each completed issue

All work was reviewed and approved by the human author before merge. Every commit includes a `Co-Authored-By: Oz <oz-agent@warp.dev>` attribution line.

## License

See [LICENSE](LICENSE) for details.
