# *** imports

# ** core
from typing import List, Tuple

# ** app
from .board_utils import BoardUtils


# *** utils

# ** util: minimax
class Minimax:
    '''
    Utility class for plain recursive minimax search.
    '''

    # * method: search (static)
    @staticmethod
    def search(board: List[int], is_maximizing: bool) -> Tuple[int, int]:
        '''
        Plain recursive minimax search.

        :param board: The current board state.
        :type board: List[int]
        :param is_maximizing: True if the current player is maximizing (X).
        :type is_maximizing: bool
        :return: A tuple of (utility value, total nodes evaluated).
        :rtype: Tuple[int, int]
        '''

        # Base case: return utility if terminal state.
        if BoardUtils.is_terminal(board):
            return BoardUtils.utility(board), 1

        # Determine the current player from maximizing flag.
        player = 1 if is_maximizing else -1

        # Initialize best value and node counter.
        node_count = 1
        if is_maximizing:
            best = float('-inf')
        else:
            best = float('inf')

        # Evaluate each successor.
        for _, child in BoardUtils.get_successors(board, player):

            # Recurse into the child state.
            value, child_nodes = Minimax.search(child, not is_maximizing)
            node_count += child_nodes

            # Update best value.
            if is_maximizing:
                best = max(best, value)
            else:
                best = min(best, value)

        # Return the best value and total nodes evaluated.
        return best, node_count

    # * method: run (static)
    @staticmethod
    def run(board: List[int]) -> Tuple[int, int]:
        '''
        Run minimax from the given board state, auto-detecting whose turn it is.

        :param board: The current board state.
        :type board: List[int]
        :return: A tuple of (utility value, total nodes evaluated).
        :rtype: Tuple[int, int]
        '''

        # Determine if the current player is maximizing.
        is_maximizing = BoardUtils.current_player(board) == 1

        # Run minimax and return the result.
        return Minimax.search(board, is_maximizing)
