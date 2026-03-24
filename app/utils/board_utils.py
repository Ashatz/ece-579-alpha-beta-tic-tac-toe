# *** imports

# ** core
from typing import List, Tuple


# *** constants

# ** constant: cell_map
CELL_MAP = {'X': 1, 'O': -1, '_': 0}

# ** constant: cell_display
CELL_DISPLAY = {1: 'X', -1: 'O', 0: '_'}

# ** constant: win_lines
WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6),              # diags
]


# *** utils

# ** util: board_utils
class BoardUtils:
    '''
    Stateless computational utility for tic-tac-toe board operations.
    '''

    # * method: parse_board (static)
    @staticmethod
    def parse_board(board_str: str) -> List[int]:
        '''
        Parse a 9-character board string into a list of integers.

        :param board_str: The board string (e.g. 'O_XOXX___').
        :type board_str: str
        :return: The board as a list of integers (X=1, O=-1, _=0).
        :rtype: List[int]
        '''

        # Convert each character to its integer representation.
        return [CELL_MAP[c] for c in board_str]

    # * method: format_board (static)
    @staticmethod
    def format_board(board: List[int]) -> str:
        '''
        Format a board list into a 3-line display string.

        :param board: The board as a list of 9 integers.
        :type board: List[int]
        :return: The formatted board string (3 rows separated by newlines).
        :rtype: str
        '''

        # Build each row by mapping cell values to display characters.
        rows = []
        for i in range(0, 9, 3):
            row = ''.join(CELL_DISPLAY[board[j]] for j in range(i, i + 3))
            rows.append(row)

        # Join rows with newlines.
        return '\n'.join(rows)

    # * method: get_successors (static)
    @staticmethod
    def get_successors(board: List[int], player: int) -> List[Tuple[int, List[int]]]:
        '''
        Generate all successor board states for the given player.

        :param board: The current board state.
        :type board: List[int]
        :param player: The player to move (1 for X, -1 for O).
        :type player: int
        :return: A list of (move_index, new_board) tuples.
        :rtype: List[Tuple[int, List[int]]]
        '''

        # Find all empty cells and generate a new board for each.
        successors = []
        for i in range(9):
            if board[i] == 0:
                new_board = board[:]
                new_board[i] = player
                successors.append((i, new_board))

        # Return the list of successors.
        return successors

    # * method: is_terminal (static)
    @staticmethod
    def is_terminal(board: List[int]) -> bool:
        '''
        Check if the board is in a terminal state (win or full).

        :param board: The current board state.
        :type board: List[int]
        :return: True if the game is over, False otherwise.
        :rtype: bool
        '''

        # Check if any player has won.
        for a, b, c in WIN_LINES:
            if board[a] == board[b] == board[c] != 0:
                return True

        # Check if the board is full (no empty cells).
        if 0 not in board:
            return True

        # Game is still in progress.
        return False

    # * method: utility (static)
    @staticmethod
    def utility(board: List[int]) -> int:
        '''
        Evaluate the utility of a terminal board state.

        :param board: The current board state.
        :type board: List[int]
        :return: 1 if X wins, -1 if O wins, 0 for draw.
        :rtype: int
        '''

        # Check each win line for a winner.
        for a, b, c in WIN_LINES:
            if board[a] == board[b] == board[c] != 0:
                return board[a]

        # No winner found — draw.
        return 0

    # * method: current_player (static)
    @staticmethod
    def current_player(board: List[int]) -> int:
        '''
        Determine the current player based on the board state.

        X always moves first, so X moves when counts are equal.

        :param board: The current board state.
        :type board: List[int]
        :return: 1 if it is X's turn, -1 if it is O's turn.
        :rtype: int
        '''

        # Count X and O pieces on the board.
        x_count = board.count(1)
        o_count = board.count(-1)

        # X moves when counts are equal, O moves otherwise.
        return 1 if x_count == o_count else -1
