from typing import Any, List


def get_integer_input(prompt: str = "Input: ") -> int:
    """ Gets command line input from the user.
        Tries as long as an integer value is provided.

        :parameter
        prompt: a string displayed to the user
    """

    while True:
        user_input = input(prompt)

        try:
            output = int(user_input)
        except ValueError:
            print("Input must be an integer!")
            continue

        break

    return output


def is_symmetric(s: list) -> bool:
    """ Checks if the provided list is symmetric

        :parameter
        s: list list of objects which will be compared. Elements of s must
            have __eq__ method implemented.
    """
    length = len(s)
    for i in range(length // 2 + 1):
        if s[i] != s[-(i + 1)]:
            return False

    return True


def is_right_size(
    board: List[List[Any]], rows: int = 7, cols: int = 7
) -> bool:
    """ Checks if the board if of size RxC

        :parameter
        board : board, whose size we want to check
        rows : desired number of rows. Default is 7.
        columns : desired number of columns. Default is 7.
    """
    if len(board) != rows:
        return False

    for row in board:
        if len(row) != cols:
            return False

    return True
