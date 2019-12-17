from .src.game import Field, Board, EntropyGame


def test_field():

    # Create an empty field
    field = Field()

    assert field.is_empty()

    # Drop a piece in the field
    field.drop_piece(1)

    assert not field.is_empty()
    assert field.piece == 1

    # Pick up a piece
    piece = field.take_piece()

    assert piece == 1
    assert field.is_empty()


def test_board_size(board=None):

    # Initialize an empty board
    board = board if board else Board()

    # Check if the board is of size 7x7
    assert len(board.fields) == 7
    for row in board.fields:
        assert len(row) == 7
        for el in row:
            # Check if each element is properly initialized
            assert isinstance(el, Field)


def test_board():

    # Initialize a board with elements
    fields = [
        [0, 0, 1, None, 2, 3, 4],
        [0, 0, 5, None, 2, 3, None],
        [None, None, 1, None, 2, None, 4],
        [0, None, 5, None, None, 3, 4],
        [None, None, 3, None, 1, None, 4],
        [0, None, 4, None, 6, 3, None],
        [0, None, None, None, 6, 2, 1],
    ]

    board = Board(board=fields)
    test_board_size(board)

    assert board.fields[0][3].is_empty()
    assert board.fields[1][3].is_empty()
    assert not board.fields[0][0].is_empty()

    # Check if putting pieces on the board works
    board.drop_piece(piece=1, row=0, col=3)
    assert not board.fields[0][3].is_empty()
    assert board.fields[0][3].piece == 1

    # Check if moving pieces on the board works
    board.move_piece(row1=0, col1=3, row2=1, col2=3)
    assert board.fields[0][3].is_empty()
    assert not board.fields[1][3].is_empty()
    assert board.fields[1][3].piece == 1


def test_game():

    fields = [
        [0, 0, 1, None, 2, 3, 4],
        [0, 0, 5, None, 2, 3, None],
        [None, None, 1, None, 2, None, 4],
        [0, None, 5, None, None, 3, 4],
        [None, None, 3, None, 1, None, 4],
        [0, None, 4, None, 6, 3, None],
        [0, None, None, None, 6, 2, 1],
    ]

    game = EntropyGame(board=fields)

    assert len(game.bag_with_pieces) == 49
