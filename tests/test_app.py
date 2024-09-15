import unittest
from copy import deepcopy
from app import is_valid_move, apply_move, check_win, has_valid_moves, INITIAL_BOARD

class TestPegSolitaire(unittest.TestCase):

    def setUp(self):
        """
        Sets up a fresh board for each test.
        """
        self.board = deepcopy(INITIAL_BOARD)

    def test_is_valid_move(self):
        """
        Test valid and invalid moves.
        """
        self.assertTrue(is_valid_move(self.board, (2, 3), (0, 3)))
        self.assertFalse(is_valid_move(self.board, (0, 0), (2, 0)))
        self.board[1][3] = 0
        self.assertFalse(is_valid_move(self.board, (2, 3), (0, 3)))
        self.board[0][3] = 1
        self.assertFalse(is_valid_move(self.board, (2, 3), (0, 3)))

    def test_apply_move(self):
        """
        Test applying a valid move.
        """
        apply_move(self.board, (2, 3), (0, 3))
        self.assertEqual(self.board[2][3], 0)
        self.assertEqual(self.board[1][3], 0)
        self.assertEqual(self.board[0][3], 1)

    def test_check_win(self):
        """
        Test winning condition with only one peg left.
        """
        win_board = [[0, 0, 0, 0, 0, 0, 0] for _ in range(7)]
        win_board[3][3] = 1
        self.assertTrue(check_win(win_board))
        self.board[3][3] = 1
        self.assertFalse(check_win(self.board))

    def test_has_valid_moves(self):
        """
        Test if there are valid moves remaining on the board.
        """
        self.assertTrue(has_valid_moves(self.board))
        no_moves_board = [[0, 0, 0, 0, 0, 0, 0] for _ in range(7)]
        no_moves_board[3][3] = 1
        self.assertFalse(has_valid_moves(no_moves_board))


if __name__ == '__main__':
    unittest.main()
