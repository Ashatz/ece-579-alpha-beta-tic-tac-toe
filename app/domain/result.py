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


# ** model: killer_move
class KillerMove(DomainObject):
    '''
    A domain object representing a killer move recorded during alpha-beta search.
    A killer move is a move that caused a cutoff at a particular depth.
    '''

    # * attribute: depth
    depth = IntegerType(required=True)

    # * attribute: move
    move = IntegerType(required=True)


# ** model: transposition_entry
class TranspositionEntry(DomainObject):
    '''
    A domain object representing an entry in the rotation-invariant transposition table.
    Stores the evaluated value for a canonical board position.
    '''

    # * attribute: canonical_board
    canonical_board = ListType(IntegerType, required=True)

    # * attribute: value
    value = IntegerType(required=True)

    # * attribute: depth
    depth = IntegerType(required=True)


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

    # * attribute: killers
    killers = ListType(ModelType(KillerMove), default=[])

    # * attribute: transpositions
    transpositions = ListType(ModelType(TranspositionEntry), default=[])
