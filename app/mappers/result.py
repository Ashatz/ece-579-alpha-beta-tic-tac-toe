# *** imports

# ** core
from typing import Dict, List, Optional, Tuple

# ** infra
from tiferet import DomainObject, Aggregate

# ** app
from ..domain.result import Cutoff, KillerMove, TranspositionEntry, GameResult


# *** mappers

# ** mapper: game_result_aggregate
class GameResultAggregate(GameResult, Aggregate):
    '''
    Mutable aggregate for game search results.
    Collects cutoff events, killer moves, and transposition entries
    during alpha-beta search.
    '''

    # * init
    def __init__(self, *args, **kwargs):
        '''
        Initialize the aggregate with internal transposition table and hit counter.
        '''

        # Call parent constructor.
        super().__init__(*args, **kwargs)

        # Internal transposition lookup table (canonical_board tuple -> value).
        self._transposition_table: Dict[Tuple[int, ...], int] = {}

        # Internal transposition hit counter.
        self._transposition_hits: int = 0

    # * method: record_cutoff
    def record_cutoff(self, board: List[int], cutoff_type: str) -> None:
        '''
        Record a pruning event. This method is passed as the on_cutoff
        callable into the alpha-beta utility.

        :param board: The board state where the cutoff occurred.
        :type board: List[int]
        :param cutoff_type: The type of cutoff ('Alpha cut' or 'Beta cut').
        :type cutoff_type: str
        '''

        # Create a new Cutoff domain object.
        cutoff = DomainObject.new(
            Cutoff,
            board=board,
            cutoff_type=cutoff_type,
        )

        # Append to the cutoffs list.
        self.cutoffs.append(cutoff)

    # * method: record_killer
    def record_killer(self, depth: int, move: int) -> None:
        '''
        Record a killer move at the given depth. This method is passed as
        the on_killer callable into the alpha-beta utility.

        :param depth: The search depth where the cutoff occurred.
        :type depth: int
        :param move: The move index (0-8) that caused the cutoff.
        :type move: int
        '''

        # Create a new KillerMove domain object.
        killer = DomainObject.new(
            KillerMove,
            depth=depth,
            move=move,
        )

        # Append to the killers list.
        self.killers.append(killer)

    # * method: get_killers_at_depth
    def get_killers_at_depth(self, depth: int) -> List[int]:
        '''
        Return the killer move indices recorded at the given depth.

        :param depth: The search depth to look up.
        :type depth: int
        :return: A list of move indices recorded as killers at this depth.
        :rtype: List[int]
        '''

        # Filter killers by depth and return move indices.
        return [k.move for k in self.killers if k.depth == depth]

    # * method: store_transposition
    def store_transposition(self, canonical_board: Tuple[int, ...], value: int, depth: int) -> None:
        '''
        Store a transposition entry for the given canonical board position.

        :param canonical_board: The canonical (rotation-invariant) board key.
        :type canonical_board: Tuple[int, ...]
        :param value: The evaluated minimax value.
        :type value: int
        :param depth: The search depth at which this was evaluated.
        :type depth: int
        '''

        # Store in the internal lookup table.
        self._transposition_table[canonical_board] = value

        # Create a TranspositionEntry domain object for the record.
        entry = DomainObject.new(
            TranspositionEntry,
            canonical_board=list(canonical_board),
            value=value,
            depth=depth,
        )

        # Append to the transpositions list.
        self.transpositions.append(entry)

    # * method: lookup_transposition
    def lookup_transposition(self, canonical_board: Tuple[int, ...]) -> Optional[int]:
        '''
        Look up a canonical board position in the transposition table.

        :param canonical_board: The canonical (rotation-invariant) board key.
        :type canonical_board: Tuple[int, ...]
        :return: The stored value if found, None otherwise.
        :rtype: Optional[int]
        '''

        # Return the stored value or None.
        return self._transposition_table.get(canonical_board)

    # * method: increment_transposition_hit
    def increment_transposition_hit(self) -> None:
        '''
        Increment the transposition hit counter.
        '''

        # Increment the counter.
        self._transposition_hits += 1

    # * property: transposition_hits
    @property
    def transposition_hits(self) -> int:
        '''
        Return the number of transposition table hits.

        :return: The transposition hit count.
        :rtype: int
        '''

        # Return the internal counter.
        return self._transposition_hits

    # * property: alpha_cuts
    @property
    def alpha_cuts(self) -> int:
        '''
        Count the number of alpha cutoffs.

        :return: The number of alpha cutoffs.
        :rtype: int
        '''

        # Count cutoffs with type 'Alpha cut'.
        return sum(1 for c in self.cutoffs if c.cutoff_type == 'Alpha cut')

    # * property: beta_cuts
    @property
    def beta_cuts(self) -> int:
        '''
        Count the number of beta cutoffs.

        :return: The number of beta cutoffs.
        :rtype: int
        '''

        # Count cutoffs with type 'Beta cut'.
        return sum(1 for c in self.cutoffs if c.cutoff_type == 'Beta cut')
