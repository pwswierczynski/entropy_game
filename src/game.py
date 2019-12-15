from random import choice
from typing import List, Optional

from termcolor import cprint

from src.utils import get_integer_input, is_right_size, is_symmetric

COLOR_MAP = {
    0: "on_red",
    1: "on_blue",
    2: "on_yellow",
    3: "on_green",
    4: "on_white",
    5: "on_magenta",
    6: "on_cyan",
}


class Field:
    """ This is a building block of the board.
        It knows, what value it has at the moment.

        :parameter
        piece : integer value representing color of a piece in this field
    """

    def __init__(self, piece: Optional[int] = None) -> None:
        self.piece = piece

    def __eq__(self, other) -> bool:
        """ Overloading the equality operator """
        if self.piece == other.piece:
            return True
        return False

    def __ne__(self, other) -> bool:
        """ Overloading not-equal operator """
        if self.piece == other.piece:
            return False
        return True

    def print_value(self) -> None:
        """ Printing out the color corresponding to the value of the field """
        if self.is_empty():
            print("X", end="")
        else:
            piece_color = COLOR_MAP[self.piece]
            cprint(" ", on_color=piece_color, end="")

    def is_empty(self) -> bool:
        """ Checks if the field is empty """
        if self.piece is None:
            return True
        return False

    def drop_piece(self, piece: int) -> None:
        """ Assigns a value to a chosen field """
        self.piece = piece

    def take_piece(self) -> Optional[int]:
        piece = self.piece
        self.piece = None

        return piece

    def __repr__(self):
        return f"Single Entropy Game piece of value {self.piece}"


class Board:
    """ This class stores only the board and not the rules of the game

        :parameter
        board : List of list of integers to initialize the fields on the board.
            It is None by default, which corresponds to an empty board.
    """

    def __init__(self, board: Optional[List[List[Optional[int]]]] = None):

        if board is None:
            board = [[None for _ in range(7)] for _ in range(7)]

        assert is_right_size(board=board), f"Board needs to be of size 7x7"

        self.fields = [[None for _ in range(7)] for _ in range(7)]
        for row in range(7):
            for col in range(7):
                piece = board[row][col]
                self.fields[row][col] = Field(piece=piece)

    @staticmethod
    def _is_inside_board(row: int, col: int) -> bool:
        """ Checks if the given coordinates belong to the board"""

        if 0 <= row <= 7 and 0 <= col <= 7:
            return True
        return False

    def transpose_board(self) -> None:
        """ Transposes the board - changes rows with cols """
        self.fields = [*zip(*self.fields)]

    def is_empty(self, row: int, col: int) -> bool:
        """ Checks if the field (row, col) on the board is taken """
        assert self._is_inside_board(
            row, col
        ), "Provide coordinates inside the board 7x7!"

        return self.fields[row][col].is_empty()

    def drop_piece(self, piece: int, row: int, col: int) -> None:

        assert self._is_inside_board(
            row, col
        ), "Provide coordinates inside the board 7x7!"

        self.fields[row][col].drop_piece(piece=piece)

    def move_piece(self, row1: int, col1: int, row2: int, col2: int):

        assert self._is_inside_board(
            row1, col1
        ), "Provide coordinates inside the board 7x7!"
        assert self._is_inside_board(
            row2, col2
        ), "Provide coordinates inside the board 7x7!"

        piece = self.fields[row1][col1].take_piece()
        self.fields[row2][col2].drop_piece(piece=piece)

    def print_board(self) -> None:

        print(" ", end="")
        for i in range(7):
            print(i, end="")
        print()

        for i, row in enumerate(self.fields):
            print(i, end="")
            for field in row:
                field.print_value()
            print()

    def get_row_subsequences(self) -> List[List[Field]]:
        """ Returns all subsequences of length at least 2
            in each row of the board. Skips empty fields.
        """

        subs = []
        for row in range(7):
            row_subs = self._row_subsequences(row=row)
            subs += row_subs

        return subs

    def _row_subsequences(self, row: int) -> List[List[Field]]:
        """ Returns all subsequences of length at least 2 in a given row.
            It filters empty spaces out.

            :parameter
            row : int choice of a row from which subsequences will be chosen
        """

        row_fields = self.fields[row]
        subs = [
            row_fields[i:j]
            for i in range(6)
            for j in range(i + 2, 8)
            if Field(None) not in row_fields[i:j]
        ]

        return subs


class EntropyGame:
    """ Class responsible for the rules of the game and for the game engine

        :parameter
        board : Board, with which the game is initialized. By default board is
            None, which corresponds to an empty game board.
    """

    def __init__(self, board=None):
        self.board = Board(board=board)
        self.bag_with_pieces = []
        for row in range(7):
            for _ in range(7):  # We need 7 of each color
                self.bag_with_pieces.append(row)

    def _score_rows(self) -> int:
        """ Computes current score in rows only
            :return:
            score : int score computed in rows only
        """
        score = 0
        row_subs = self.board.get_row_subsequences()
        for row_sub in row_subs:
            if is_symmetric(row_sub):
                score += len(row_sub)

        return score

    def _score_cols(self) -> int:
        """ Computes current score in cols only
            We do this by turning the board and using _score_rows function
            :return:
            score : int score computed in cols only
        """
        self.board.transpose_board()
        score = self._score_rows()
        self.board.transpose_board()

        return score

    def score(self) -> int:
        """ Computes current score of the entropy game.
            This function loops over all sequences in rows and cols
            of fields checks if they are symmetric. It adds the lengths of each
            symmetric sequence to the score.
        """
        score = self._score_rows()
        score += self._score_cols()

        return score

    def _pick_a_piece(self) -> int:
        """ Method responsible for randomly choosing a block fror a bag """

        n_pieces_in_bag = len(self.bag_with_pieces)
        idx = choice(range(n_pieces_in_bag))

        piece = self.bag_with_pieces.pop(idx)

        return piece

    def place_a_piece(self, piece: int, row: int, col: int) -> bool:
        """ This method puts a piece on a given field.
            It assumes that the input is admissible.

            :parameters
            piece - value of the piece
            row - row of the desired possition of the block
            col - column of the desired possition of the block
        """
        self.board.drop_piece(piece=piece, row=row, col=col)

        return True

    def _is_move_admissible(
        self, row1: int, col1: int, row2: int, col2: int
    ) -> bool:
        """ This function checks if the pieces move only along vertical
            and horizontal axes. It also checks if there are no pieces
            between the origin and the destination of the moved piece.
        """

        if row1 != row2 and col1 != col2:
            return False

        if row1 < row2:
            for row in range(row1 + 1, row2 + 1):
                if not self.board.is_empty(row, col1):
                    return False

        if row1 > row2:
            for row in range(row2, row1):
                if not self.board.is_empty(row, col1):
                    return False

        if col1 < col2:
            for col in range(col1 + 1, col2 + 1):
                if not self.board.is_empty(row1, col):
                    return False

        if col1 > col2:
            for col in range(col2, col1):
                if not self.board.is_empty(row1, col):
                    return False

        return True

    def move_piece(self, row1: int, col1: int, row2: int, col2: int) -> bool:
        """ This method performs an Order move.
            It assumes that the input is admissible.

            :parameters
            row1 - row of the initial possition of the block
            col1 - column of the initial possition of the block
            row2 - row of the final possition of the block
            col2 - column of the final possition of the block
        """

        self.board.move_piece(row1=row1, col1=col1, row2=row2, col2=col2)

        return True

    def _move_chaos(self) -> None:
        """ Perform a complete move by chaos consisting of
            picking up a piece from a bag and placing it on the board.

            This method allows only admissible moves.
        """

        piece = self._pick_a_piece()
        piece_color = COLOR_MAP[piece]
        print("You picked: ", end="")
        cprint(" ", on_color=piece_color)

        while True:

            row = get_integer_input(
                prompt="In which row would you like to place the piece? "
            )
            col = get_integer_input(
                prompt="In which column would you like to place the piece? "
            )

            if not self.board._is_inside_board(row=row, col=col):
                print("Given coordinates are outside the board! Try again!")
                continue

            if not self.board.is_empty(row=row, col=col):
                print("This field is occupied! Try again!")
                continue

            break

        self.place_a_piece(piece=piece, row=int(row), col=int(col))

    def _move_order(self) -> None:
        """ Performs a complete move by order. It can either move a piece
            on the board or pass.

            This method allows only admissible moves.
        """
        while True:

            row1 = get_integer_input(
                prompt="Row of the piece you want to move: "
            )
            col1 = get_integer_input(
                prompt="Column of the piece you want to move: "
            )

            if not self.board._is_inside_board(row=row1, col=col1):
                print("Given coordinates are outside the board! Try again!")
                continue

            if self.board.is_empty(row=row1, col=col1):
                print("This field is empty! Try again!")
                continue

            row2 = get_integer_input(prompt="Row of the destination: ")
            col2 = get_integer_input(prompt="Column of the destination: ")

            if not self.board._is_inside_board(row=row1, col=col1):
                print("Given coordinates are outside the board! Try again!")
                continue

            if not self._is_move_admissible(
                row1=row1, col1=col1, row2=row2, col2=col2
            ):
                print("This move is not admissible! Try again!")
                continue

            break

        self.move_piece(row1=row1, col1=col1, row2=row2, col2=col2)

    def play(self) -> None:

        for _ in range(49):

            self.board.print_board()
            print("Current score: ", self.score())
            self._move_chaos()

            self.board.print_board()
            print("Current score: ", self.score())
            self._move_order()

        self.board.print_board()
        print("Final score: ", self.score())
