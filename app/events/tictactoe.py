# *** imports

# ** core
from typing import Any, Dict, List

# ** infra
from tiferet import DomainEvent, Aggregate

# ** app
from ..utils.board_utils import BoardUtils
from ..utils.minimax import Minimax
from ..utils.alphabeta import AlphaBeta
from ..mappers.result import GameResultAggregate


# *** events

# ** event: solve_tic_tac_toe
class SolveTicTacToe(DomainEvent):
    '''
    Domain event to solve a tic-tac-toe board using Minimax and Alpha-Beta pruning.
    '''

    # * method: execute
    @DomainEvent.parameters_required(['board'])
    def execute(self, board: str, **kwargs) -> Dict[str, Any]:
        '''
        Execute the solve event.

        :param board: A 9-character board string (X, O, _).
        :type board: str
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: A dict with board, minimax_result, and alphabeta_result.
        :rtype: Dict[str, Any]
        '''

        # Validate board string length.
        self.verify(
            len(board) == 9,
            'INVALID_INPUT',
            f'Board must be exactly 9 characters, got {len(board)}',
            board=board,
        )

        # Validate board string characters.
        self.verify(
            all(c in ('X', 'O', '_') for c in board),
            'INVALID_INPUT',
            f'Board must contain only X, O, or _ characters',
            board=board,
        )

        # Parse the board string into a list of integers.
        cells = BoardUtils.parse_board(board)

        # Run plain minimax search.
        mm_value, mm_nodes = Minimax.run(cells)

        # Create a GameResultAggregate for the minimax result.
        minimax_result = Aggregate.new(
            GameResultAggregate,
            value=mm_value,
            nodes=mm_nodes,
            algorithm='minimax',
            cutoffs=[],
        )

        # Create a GameResultAggregate for the alpha-beta result.
        # Initialize with placeholder values; will be updated after search.
        ab_result = Aggregate.new(
            GameResultAggregate,
            value=0,
            nodes=0,
            algorithm='alphabeta',
            cutoffs=[],
            validate=False,
        )

        # Run alpha-beta search with the aggregate's record_cutoff as callback.
        ab_value, ab_nodes = AlphaBeta.run(cells, on_cutoff=ab_result.record_cutoff)

        # Update the alpha-beta aggregate with final values.
        ab_result.set_attribute('value', ab_value)
        ab_result.set_attribute('nodes', ab_nodes)

        # Return results dict for downstream events.
        return dict(
            board=cells,
            minimax_result=minimax_result,
            alphabeta_result=ab_result,
        )


# ** event: print_results
class PrintResults(DomainEvent):
    '''
    Domain event to format and print tic-tac-toe solver results per homework spec.
    '''

    # * method: execute
    @DomainEvent.parameters_required(['results'])
    def execute(self, results: Dict[str, Any], **kwargs) -> None:
        '''
        Format and print the solver results to stdout.

        :param results: A dict containing board, minimax_result, and alphabeta_result.
        :type results: Dict[str, Any]
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: None
        :rtype: None
        '''

        # Extract results components.
        board = results['board']
        minimax_result: GameResultAggregate = results['minimax_result']
        ab_result: GameResultAggregate = results['alphabeta_result']

        # Print the initial board.
        print(BoardUtils.format_board(board))

        # Print minimax results.
        print(f'Game Result: {minimax_result.value}')
        print(f'Moves considered without alpha-beta pruning: {minimax_result.nodes}')

        # Print each alpha-beta cutoff (board + cutoff type).
        for i, cutoff in enumerate(ab_result.cutoffs):
            if i > 0:
                print()
            print(BoardUtils.format_board(cutoff.board))
            print(cutoff.cutoff_type)

        # Print alpha-beta summary stats.
        print(f'Game Result: {ab_result.value}')
        print(f'Moves considered with alpha-beta pruning: {ab_result.nodes}')
        print(f'Alpha cuts: {ab_result.alpha_cuts}')
        print(f'Beta cuts: {ab_result.beta_cuts}')

        # Return empty string to suppress CLI 'None' output.
        return ''
