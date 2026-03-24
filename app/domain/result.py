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
    A domain object representing a single alpha-beta pruning event.
    '''

    # * attribute: board
    board = ListType(IntegerType, required=True)

    # * attribute: cutoff_type
    cutoff_type = StringType(required=True)


# ** model: game_result
class GameResult(DomainObject):
    '''
    A domain object representing the result of a game search algorithm.
    '''

    # * attribute: value
    value = IntegerType(required=True)

    # * attribute: nodes
    nodes = IntegerType(required=True)

    # * attribute: algorithm
    algorithm = StringType(required=True)

    # * attribute: cutoffs
    cutoffs = ListType(ModelType(Cutoff), default=[])
