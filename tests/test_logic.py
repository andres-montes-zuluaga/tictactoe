import unittest
from src.logic import Board

class TestBoard(unittest.TestCase):
    """
    Unittest for the Board class in src/logic.py.
    Tests basic board behavior: init, moves, turn rotation, victory, and draw.
    """

    def setUp(self):
        """Set up a new empty board before every test."""
        self.board = Board(size=3)

    def test_init_board(self):
        """Board is empty and turn is X on initialization."""
        for row in self.board.grid:
            self.assertEqual(row, ["", "", ""])
        self.assertEqual(self.board.turn, "X")

    def test_make_move_and_turn_switch(self):
        """Making a valid move updates the board and switches turns."""
        self.assertTrue(self.board.make_move(0, 0))  # X
        self.assertEqual(self.board.grid[0][0], "X")
        self.assertEqual(self.board.turn, "O")
        self.assertTrue(self.board.make_move(1, 1))  # O
        self.assertEqual(self.board.grid[1][1], "O")
        self.assertEqual(self.board.turn, "X")

    def test_invalid_move(self):
        """Invalid moves (out of bounds or duplicate) return False."""
        self.assertFalse(self.board.make_move(3, 0))
        self.assertFalse(self.board.make_move(-1, 2))
        self.board.make_move(0, 0)
        self.assertFalse(self.board.make_move(0, 0))  # Square already taken

    def test_check_row_winner(self):
        """Rows produce a win when filled by same mark."""
        for col in range(3):
            self.board.grid[1][col] = "O"
        self.assertEqual(self.board.check_winner(), "O")

    def test_check_column_winner(self):
        """Columns produce a win when filled by same mark."""
        for row in range(3):
            self.board.grid[row][2] = "X"
        self.assertEqual(self.board.check_winner(), "X")

    def test_check_diagonal_winner(self):
        """Diagonals produce a win when filled by same mark."""
        for idx in range(3):
            self.board.grid[idx][idx] = "O"
        self.assertEqual(self.board.check_winner(), "O")
        self.board.reset()
        for idx in range(3):
            self.board.grid[idx][2-idx] = "X"
        self.assertEqual(self.board.check_winner(), "X")

    def test_draw(self):
        """A full board with no winner is a draw."""
        filled = [
            ["X", "O", "X"],
            ["X", "O", "O"],
            ["O", "X", "X"]
        ]
        self.board.grid = filled
        self.assertIsNone(self.board.check_winner())
        self.assertTrue(self.board.is_full())

    def test_reset(self):
        """reset() function clears the board and resets turn."""
        self.board.make_move(0, 0)
        self.board.make_move(1, 1)
        self.board.reset()
        for row in self.board.grid:
            self.assertEqual(row, ["", "", ""])
        self.assertEqual(self.board.turn, "X")

if __name__ == '__main__':
    unittest.main()
