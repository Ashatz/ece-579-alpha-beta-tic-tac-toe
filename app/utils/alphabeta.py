# *** imports

# ** core
from typing import List, Tuple, Callable, Optional

# ** app
from .board_utils import BoardUtils


# *** utils

# ** util: alphabeta
class AlphaBeta:
    '''
    Utility class for alpha-beta pruning search with optional killer heuristic
    and rotation-invariant transposition table support.
    Pure computation with no side effects — all state interaction
    occurs through callbacks.
    '''

    # * method: _reorder_successors (static)
    @staticmethod
    def _reorder_successors(successors: List[Tuple[int, List[int]]],
            killer_moves: List[int]) -> List[Tuple[int, List[int]]]:
        '''
        Reorder successors so killer moves are tried first.

        :param successors: The list of (move_index, new_board) tuples.
        :type successors: List[Tuple[int, List[int]]]
        :param killer_moves: Move indices to prioritize.
        :type killer_moves: List[int]
        :return: Reordered successors with killer moves first.
        :rtype: List[Tuple[int, List[int]]]
        '''

        # Separate killer and non-killer successors.
        killers_first = [s for s in successors if s[0] in killer_moves]
        rest = [s for s in successors if s[0] not in killer_moves]

        # Return killer moves followed by remaining moves.
        return killers_first + rest

    # * method: search (static)
    @staticmethod
    def search(board: List[int],
            alpha: float,
            beta: float,
            is_maximizing: bool,
            depth: int = 0,
            on_cutoff: Optional[Callable] = None,
            on_killer: Optional[Callable] = None,
            get_killers: Optional[Callable] = None,
            lookup_transposition: Optional[Callable] = None,
            store_transposition: Optional[Callable] = None,
            on_transposition_hit: Optional[Callable] = None) -> Tuple[int, int]:
        '''
        Alpha-beta pruning search with optional killer heuristic and
        transposition table support.

        :param board: The current board state.
        :type board: List[int]
        :param alpha: The alpha bound.
        :type alpha: float
        :param beta: The beta bound.
        :type beta: float
        :param is_maximizing: True if the current player is maximizing (X).
        :type is_maximizing: bool
        :param depth: The current search depth (0 at root).
        :type depth: int
        :param on_cutoff: Optional callback invoked on pruning: on_cutoff(board, cutoff_type).
        :type on_cutoff: Optional[Callable]
        :param on_killer: Optional callback to record a killer move: on_killer(depth, move).
        :type on_killer: Optional[Callable]
        :param get_killers: Optional callback to get killer moves: get_killers(depth) -> List[int].
        :type get_killers: Optional[Callable]
        :param lookup_transposition: Optional callback: lookup_transposition(canonical_board) -> int | None.
        :type lookup_transposition: Optional[Callable]
        :param store_transposition: Optional callback: store_transposition(canonical_board, value, depth).
        :type store_transposition: Optional[Callable]
        :param on_transposition_hit: Optional callback invoked on a transposition hit.
        :type on_transposition_hit: Optional[Callable]
        :return: A tuple of (utility value, total nodes evaluated).
        :rtype: Tuple[int, int]
        '''

        # Base case: return utility if terminal state.
        if BoardUtils.is_terminal(board):
            return BoardUtils.utility(board), 1

        # Check transposition table before expanding.
        if lookup_transposition:
            canonical = BoardUtils.get_canonical_board(board)
            cached_value = lookup_transposition(canonical)
            if cached_value is not None:
                if on_transposition_hit:
                    on_transposition_hit()
                return cached_value, 1

        # Determine the current player from maximizing flag.
        player = 1 if is_maximizing else -1

        # Generate successors and apply killer move ordering.
        successors = BoardUtils.get_successors(board, player)
        if get_killers:
            killer_moves = get_killers(depth)
            if killer_moves:
                successors = AlphaBeta._reorder_successors(successors, killer_moves)

        # Initialize node counter.
        node_count = 1

        # Bundle callback arguments for recursive calls.
        cb_kwargs = dict(
            on_cutoff=on_cutoff,
            on_killer=on_killer,
            get_killers=get_killers,
            lookup_transposition=lookup_transposition,
            store_transposition=store_transposition,
            on_transposition_hit=on_transposition_hit,
        )

        # Maximizing player logic.
        if is_maximizing:
            best = float('-inf')
            did_cutoff = False

            for move, child in successors:

                # Recurse into the child state.
                value, child_nodes = AlphaBeta.search(
                    child, alpha, beta, False, depth + 1, **cb_kwargs)
                node_count += child_nodes

                # Update best value and alpha.
                best = max(best, value)
                alpha = max(alpha, best)

                # Beta cutoff: prune remaining branches.
                if alpha >= beta:
                    if on_cutoff:
                        on_cutoff(board, 'Beta cut')
                    if on_killer:
                        on_killer(depth, move)
                    did_cutoff = True
                    break

            # Only store exact values (fully explored nodes) in transposition table.
            if store_transposition and not did_cutoff:
                canonical = BoardUtils.get_canonical_board(board)
                store_transposition(canonical, best, depth)

            return best, node_count

        # Minimizing player logic.
        else:
            best = float('inf')
            did_cutoff = False

            for move, child in successors:

                # Recurse into the child state.
                value, child_nodes = AlphaBeta.search(
                    child, alpha, beta, True, depth + 1, **cb_kwargs)
                node_count += child_nodes

                # Update best value and beta.
                best = min(best, value)
                beta = min(beta, best)

                # Alpha cutoff: prune remaining branches.
                if beta <= alpha:
                    if on_cutoff:
                        on_cutoff(board, 'Alpha cut')
                    if on_killer:
                        on_killer(depth, move)
                    did_cutoff = True
                    break

            # Only store exact values (fully explored nodes) in transposition table.
            if store_transposition and not did_cutoff:
                canonical = BoardUtils.get_canonical_board(board)
                store_transposition(canonical, best, depth)

            return best, node_count

    # * method: run (static)
    @staticmethod
    def run(board: List[int],
            on_cutoff: Optional[Callable] = None,
            on_killer: Optional[Callable] = None,
            get_killers: Optional[Callable] = None,
            lookup_transposition: Optional[Callable] = None,
            store_transposition: Optional[Callable] = None,
            on_transposition_hit: Optional[Callable] = None) -> Tuple[int, int]:
        '''
        Run alpha-beta search from the given board state, auto-detecting whose turn it is.

        :param board: The current board state.
        :type board: List[int]
        :param on_cutoff: Optional callback invoked on pruning events.
        :type on_cutoff: Optional[Callable]
        :param on_killer: Optional callback to record a killer move.
        :type on_killer: Optional[Callable]
        :param get_killers: Optional callback to get killer moves at a depth.
        :type get_killers: Optional[Callable]
        :param lookup_transposition: Optional callback for transposition lookup.
        :type lookup_transposition: Optional[Callable]
        :param store_transposition: Optional callback for transposition storage.
        :type store_transposition: Optional[Callable]
        :param on_transposition_hit: Optional callback for transposition hit counting.
        :type on_transposition_hit: Optional[Callable]
        :return: A tuple of (utility value, total nodes evaluated).
        :rtype: Tuple[int, int]
        '''

        # Determine if the current player is maximizing.
        is_maximizing = BoardUtils.current_player(board) == 1

        # Run alpha-beta with initial bounds and all callbacks.
        return AlphaBeta.search(
            board, float('-inf'), float('inf'), is_maximizing,
            depth=0,
            on_cutoff=on_cutoff,
            on_killer=on_killer,
            get_killers=get_killers,
            lookup_transposition=lookup_transposition,
            store_transposition=store_transposition,
            on_transposition_hit=on_transposition_hit,
        )
