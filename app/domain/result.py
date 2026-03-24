# *** imports

# ** infra
from tiferet import (
    DomainObject,
    IntegerType,
    StringType,
    ListType,
    ModelType,
)


# *** models

# ** model: cutoff
class Cutoff(DomainObject):
    '''
    Read-only domain object representing a single alpha-beta cutoff event.
    '''

    # * attribute: board
    board = ListType(IntegerType, required=True)

    # * attribute: cutoff_type
    cutoff_type = StringType(required=True)


# ** model: game_result
class GameResult(DomainObject):
    '''
    Read-only domain object representing the outcome of a minimax or alpha-beta search.
    '''

    # * attribute: value
    value = IntegerType(required=True)

    # * attribute: nodes
    nodes = IntegerType(required=True)

    # * attribute: algorithm
    algorithm = StringType(required=True)

    # * attribute: cutoffs
    cutoffs = ListType(ModelType(Cutoff), default=[])
