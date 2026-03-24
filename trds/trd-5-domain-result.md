# Technical Requirements Document: Domain — Cutoff, GameResult & GameResultAggregate

**Project:** ECE 479/579 Tic-Tac-Toe Solver
**Repository:** https://github.com/your-org/ece-579-alpha-beta-tic-tac-toe
**Date:** March 24, 2026
**Version:** 0.1.0

## 1. Overview

Define the result bounded context: `Cutoff` and `GameResult` as read-only domain objects in a single module, and `GameResultAggregate` as the mutable extension that collects cutoff events during alpha-beta search. The aggregate's `record_cutoff` method serves as the callable injected into the `AlphaBeta` utility, making the aggregate the single point of mutation.

## 2. Scope

### In Scope
- `Cutoff` and `GameResult` domain objects in `app/domain/result.py`.
- `GameResultAggregate` in `app/mappers/result.py` with `record_cutoff` method and derived properties.
- Package init file `app/mappers/__init__.py`.
- User-facing guide at `docs/guides/domain/result.md`.

### Out of Scope
- Search algorithms — covered in TRDs 2–3.
- Domain events that consume these objects — covered in TRD 6.

## 3. Components Affected

| Component | File/Path | Changes |
|-----------|-----------|---------|
| Cutoff | `app/domain/result.py` | New domain object |
| GameResult | `app/domain/result.py` | New domain object |
| GameResultAggregate | `app/mappers/result.py` | New aggregate |
| Package init | `app/mappers/__init__.py` | New file — empty |
| Guide | `docs/guides/domain/result.md` | New file — usage guide |

## 4. Detailed Requirements

### 4.1 Cutoff (DomainObject)
- **`board`** — `ListType(IntegerType)`, required. Board state where cutoff occurred.
- **`cutoff_type`** — `StringType`, required. `'Alpha cut'` or `'Beta cut'`.

### 4.2 GameResult (DomainObject)
- **`value`** — `IntegerType`, required. Utility value.
- **`nodes`** — `IntegerType`, required. Nodes evaluated.
- **`algorithm`** — `StringType`, required. `'minimax'` or `'alphabeta'`.
- **`cutoffs`** — `ListType(ModelType(Cutoff))`, default `[]`.

### 4.3 GameResultAggregate (GameResult, Aggregate)
- **`record_cutoff(board: List[int], cutoff_type: str)`** — Creates a `Cutoff` via `DomainObject.new()` and appends to `self.cutoffs`. This method is passed as the `on_cutoff` callback into `AlphaBeta.run()`.
- **`alpha_cuts`** (property) — `sum(1 for c in self.cutoffs if c.cutoff_type == 'Alpha cut')`.
- **`beta_cuts`** (property) — `sum(1 for c in self.cutoffs if c.cutoff_type == 'Beta cut')`.

### 4.4 Bounded Context Design
`Cutoff` and `GameResult` share the same module (`result.py`) because `Cutoff` is structurally part of the result — it only exists within the context of a game result's cutoff list.

### 4.5 Code Style
- Domain: `# *** models` / `# ** model: cutoff` / `# ** model: game_result`.
- Mapper: `# *** mappers` / `# ** mapper: game_result_aggregate` / `# * method: record_cutoff` / `# * property: alpha_cuts`.

## 5. Acceptance Criteria

1. `DomainObject.new(Cutoff, board=[...], cutoff_type='Alpha cut')` creates a valid instance.
2. `Aggregate.new(GameResultAggregate, value=0, nodes=0, algorithm='alphabeta', cutoffs=[])` creates a valid instance.
3. `aggregate.record_cutoff([...], 'Beta cut')` appends a `Cutoff` to `self.cutoffs`.
4. `aggregate.alpha_cuts` and `aggregate.beta_cuts` return correct counts.
5. Both domain objects and the aggregate follow structured code style.
6. Guide document exists at `docs/guides/domain/result.md`.

## 6. Non-Functional Requirements

- Domain objects are read-only — mutation only through the aggregate.
- Aggregate uses `DomainObject.new()` for Cutoff creation (not raw constructor).
- Consistent with Tiferet structured code style.

## Related Code Style Documentation

- [code_style.md](https://github.com/greatstrength/tiferet/blob/v2.0-proto/docs/core/code_style.md)
- [domain.md](https://github.com/greatstrength/tiferet/blob/v2.0-proto/docs/core/domain.md)
- [mappers.md](https://github.com/greatstrength/tiferet/blob/v2.0-proto/docs/core/mappers.md)
