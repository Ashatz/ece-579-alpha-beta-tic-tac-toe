# *** imports

# ** infra
from tiferet import DomainObject, ListType, IntegerType


# *** models

# ** model: tic_tac_toe_board
class TicTacToeBoard(DomainObject):
    '''
    A domain object representing a tic-tac-toe board state.
    '''

    # * attribute: cells
    cells = ListType(IntegerType, required=True)

    # * attribute: current_player
    current_player = IntegerType(required=True)
