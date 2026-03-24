# *** imports

# ** core
from typing import List

# ** infra
from tiferet import DomainObject, Aggregate

# ** app
from ..domain.result import Cutoff, GameResult


# *** mappers

# ** mapper: game_result_aggregate
class GameResultAggregate(GameResult, Aggregate):
    '''
    Mutable aggregate for game search results.
    Collects cutoff events during alpha-beta search.
    '''

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
