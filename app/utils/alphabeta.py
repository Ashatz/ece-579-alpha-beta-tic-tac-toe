# *** imports

# ** core
from typing import List, Tuple, Callable, Optional

# ** app
from .board_utils import BoardUtils


# *** utils

# ** util: alphabeta
class AlphaBeta:
    '''
    Stateless computational utility implementing alpha-beta pruning for tic-tac-toe.
    '''

    # * method: search (static)
    @staticmethod
    def search(board: List[int],
            alpha: float,
            beta: float,
            is_maximizing: bool,
            on_cutoff: Optional[Callable] = None) -> Tuple[int, int]:
        '''
        Alpha-beta pruning search.

        When a cutoff occurs, calls on_cutoff(board, cutoff_type) if provided,
        where board is the parent board state at the current recursive call.

        :param board: The current board state.
        :type board: List[int]
        :param alpha: The alpha bound.
        :type alpha: float
        :param beta: The beta bound.
        :type beta: float
        :param is_maximizing: True if the current player is maximizing (X).
        :type is_maximizing: bool
        :param on_cutoff: Optional callback invoked on pruning events.
        :type on_cutoff: Optional[Callable]
        :return: A tuple of (utility value, total nodes evaluated).
        :rtype: Tuple[int, int]
        '''

        # Base case: return utility if terminal state.
        if BoardUtils.is_terminal(board):
            return BoardUtils.utility(board), 1

        # Determine the current player from maximizing flag.
        player = 1 if is_maximizing else -1

        # Initialize node counter.
        node_count = 1

        # Maximizing player logic.
        if is_maximizing:
            best = float('-inf')

            for _, child in BoardUtils.get_successors(board, player):

                # Recurse into the child state.
                value, child_nodes = AlphaBeta.search(child, alpha, beta, False, on_cutoff)
                node_count += child_nodes

                # Update best value and alpha.
                best = max(best, value)
                alpha = max(alpha, best)

                # Beta cutoff: prune remaining branches.
                if alpha >= beta:
                    if on_cutoff:
                        on_cutoff(board, 'Beta cut')
                    break

            return best, node_count

        # Minimizing player logic.
        else:
            best = float('inf')

            for _, child in BoardUtils.get_successors(board, player):

                # Recurse into the child state.
                value, child_nodes = AlphaBeta.search(child, alpha, beta, True, on_cutoff)
                node_count += child_nodes

                # Update best value and beta.
                best = min(best, value)
                beta = min(beta, best)

                # Alpha cutoff: prune remaining branches.
                if beta <= alpha:
                    if on_cutoff:
                        on_cutoff(board, 'Alpha cut')
                    break

            return best, node_count

    # * method: run (static)
    @staticmethod
    def run(board: List[int],
            on_cutoff: Optional[Callable] = None) -> Tuple[int, int]:
        '''
        Run alpha-beta search from the given board state, auto-detecting whose turn it is.

        :param board: The current board state.
        :type board: List[int]
        :param on_cutoff: Optional callback invoked on pruning events.
        :type on_cutoff: Optional[Callable]
        :return: A tuple of (utility value, total nodes evaluated).
        :rtype: Tuple[int, int]
        '''

        # Determine if the current player is maximizing.
        is_maximizing = BoardUtils.current_player(board) == 1

        # Run alpha-beta with initial bounds.
        return AlphaBeta.search(board, float('-inf'), float('inf'), is_maximizing, on_cutoff)
