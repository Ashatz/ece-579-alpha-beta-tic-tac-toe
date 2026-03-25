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
    Domain event that runs four search algorithm variants and collects results.
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
        :return: A dict with board and all four algorithm results.
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

        # --- 1. Plain Minimax ---
        mm_value, mm_nodes = Minimax.run(cells)

        # Create a GameResultAggregate for the minimax result.
        minimax_result = Aggregate.new(
            GameResultAggregate,
            value=mm_value,
            nodes=mm_nodes,
            algorithm='minimax',
            cutoffs=[],
        )

        # --- 2. Plain Alpha-Beta (cutoffs only) ---
        ab_result = Aggregate.new(
            GameResultAggregate,
            value=0, nodes=0, algorithm='alphabeta',
            cutoffs=[], killers=[], transpositions=[],
            validate=False,
        )

        # Run plain alpha-beta with cutoff recording only.
        ab_value, ab_nodes = AlphaBeta.run(
            cells,
            on_cutoff=ab_result.record_cutoff,
        )

        # Update the plain alpha-beta aggregate with final values.
        ab_result.set_attribute('value', ab_value)
        ab_result.set_attribute('nodes', ab_nodes)

        # --- 3. Alpha-Beta + Killer Heuristic ---
        killer_result = Aggregate.new(
            GameResultAggregate,
            value=0, nodes=0, algorithm='alphabeta_killer',
            cutoffs=[], killers=[], transpositions=[],
            validate=False,
        )

        # Run alpha-beta with killer heuristic (no transposition table).
        k_value, k_nodes = AlphaBeta.run(
            cells,
            on_cutoff=killer_result.record_cutoff,
            on_killer=killer_result.record_killer,
            get_killers=killer_result.get_killers_at_depth,
        )

        # Update the killer heuristic aggregate with final values.
        killer_result.set_attribute('value', k_value)
        killer_result.set_attribute('nodes', k_nodes)

        # --- 4. Alpha-Beta + Killer + Transposition Table ---
        trans_result = Aggregate.new(
            GameResultAggregate,
            value=0, nodes=0, algorithm='alphabeta_killer_trans',
            cutoffs=[], killers=[], transpositions=[],
            validate=False,
        )

        # Run alpha-beta with killer heuristic and transposition table.
        t_value, t_nodes = AlphaBeta.run(
            cells,
            on_cutoff=trans_result.record_cutoff,
            on_killer=trans_result.record_killer,
            get_killers=trans_result.get_killers_at_depth,
            lookup_transposition=trans_result.lookup_transposition,
            store_transposition=trans_result.store_transposition,
            on_transposition_hit=trans_result.increment_transposition_hit,
        )

        # Update the transposition aggregate with final values.
        trans_result.set_attribute('value', t_value)
        trans_result.set_attribute('nodes', t_nodes)

        # Return results dict for downstream events.
        return dict(
            board=cells,
            minimax_result=minimax_result,
            alphabeta_result=ab_result,
            killer_result=killer_result,
            transposition_result=trans_result,
        )


# ** event: print_results
class PrintResults(DomainEvent):
    '''
    Domain event that formats and prints search results for all four algorithm variants.
    '''

    # * method: execute
    @DomainEvent.parameters_required(['results'])
    def execute(self, results: Dict[str, Any], **kwargs) -> str:
        '''
        Format and print the solver results to stdout.

        :param results: A dict containing board and all four algorithm results.
        :type results: Dict[str, Any]
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: Empty string to suppress CLI None output.
        :rtype: str
        '''

        # Extract results components.
        board = results['board']
        minimax_result: GameResultAggregate = results['minimax_result']
        ab_result: GameResultAggregate = results['alphabeta_result']
        killer_result: GameResultAggregate = results['killer_result']
        trans_result: GameResultAggregate = results['transposition_result']

        # Print the initial board.
        print(BoardUtils.format_board(board))

        # Print minimax results.
        print(f'Game Result: {minimax_result.value}')
        print(f'Moves considered without alpha-beta pruning: {minimax_result.nodes}')

        # Print each plain alpha-beta cutoff (board + cutoff type).
        for i, cutoff in enumerate(ab_result.cutoffs):
            if i > 0:
                print()
            print(BoardUtils.format_board(cutoff.board))
            print(cutoff.cutoff_type)

        # Print plain alpha-beta summary stats.
        print(f'Game Result: {ab_result.value}')
        print(f'Moves considered with alpha-beta pruning: {ab_result.nodes}')
        print(f'Alpha cuts: {ab_result.alpha_cuts}')
        print(f'Beta cuts: {ab_result.beta_cuts}')

        # Print killer heuristic summary stats.
        print(f'Game Result: {killer_result.value}')
        print(f'Moves considered with killer heuristic: {killer_result.nodes}')
        print(f'Alpha cuts: {killer_result.alpha_cuts}')
        print(f'Beta cuts: {killer_result.beta_cuts}')

        # Print rotation invariance (transposition table) summary stats.
        print(f'Game Result: {trans_result.value}')
        print(f'Moves considered with rotation invariance: {trans_result.nodes}')
        print(f'Transposition hits: {trans_result.transposition_hits}')
        print(f'Alpha cuts: {trans_result.alpha_cuts}')
        print(f'Beta cuts: {trans_result.beta_cuts}')

        # Return empty string to suppress CLI 'None' output.
        return ''
