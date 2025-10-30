"""
Unit tests for the Board and Player classes in src.logic.

These tests verify correct board initialization, move validation, win/draw detection,
and player statistics management. Each test is documented for clarity of expected behavior.
"""

import unittest
from src.logic import Board, Player

class TestBoard(unittest.TestCase):
    """Tests for the Board class logic and rules."""

    def setUp(self):
        """Initialize a new empty board before each test."""
        self.board = Board()

    def test_initial_board_empty(self):
        """
        The board should be empty (all cells '') upon initialization.
        """
        for row in self.board.grid:
            for cell in row:
                self.assertEqual(cell, '')

    def test_make_valid_move(self):
        """
        Making a move in a free cell should succeed and update the grid.
        """
        result = self.board.make_move(0, 0, 'X')
        self.assertTrue(result)
        self.assertEqual(self.board.grid[0][0], 'X')

    def test_make_invalid_move(self):
        """
        Making a move in an occupied cell should fail and not overwrite the existing value.
        """
        self.board.make_move(1, 1, 'O')
        result = self.board.make_move(1, 1, 'X')
        self.assertFalse(result)
        self.assertEqual(self.board.grid[1][1], 'O')

    def test_check_winner_row(self):
        """
        Filling a row with the same mark should declare a winner.
        """
        for i in range(self.board.size):
            self.board.make_move(0, i, 'X')
        self.assertEqual(self.board.check_winner(), 'X')

    def test_check_winner_column(self):
        """
        Filling a column with the same mark should declare a winner.
        """
        for i in range(self.board.size):
            self.board.make_move(i, 1, 'O')
        self.assertEqual(self.board.check_winner(), 'O')

    def test_check_winner_diagonal(self):
        """
        Filling a diagonal with the same mark should declare a winner.
        """
        for i in range(self.board.size):
            self.board.make_move(i, i, 'X')
        self.assertEqual(self.board.check_winner(), 'X')

    def test_check_winner_antidiagonal(self):
        """
        Filling the anti-diagonal with the same mark should declare a winner.
        """
        size = self.board.size
        for i in range(size):
            self.board.make_move(i, size - 1 - i, 'O')
        self.assertEqual(self.board.check_winner(), 'O')

    def test_draw(self):
        """
        Filling the board with no winner should result in a draw.
        """
        moves = [
            (0, 0, 'X'), (0, 1, 'O'), (0, 2, 'X'),
            (1, 0, 'O'), (1, 1, 'X'), (1, 2, 'O'),
            (2, 0, 'O'), (2, 1, 'X'), (2, 2, 'O'),
        ]
        for row, col, mark in moves:
            self.board.make_move(row, col, mark)
        self.assertTrue(self.board.check_draw())
        self.assertIsNone(self.board.check_winner())

class TestPlayer(unittest.TestCase):
    """Tests for the Player class statistics and methods."""

    def setUp(self):
        """Initialize a player before each test."""
        self.player = Player("Alice", "X")

    def test_initial_stats(self):
        """Player stats should be zero at the start."""
        self.assertEqual(self.player.wins, 0)
        self.assertEqual(self.player.losses, 0)
        self.assertEqual(self.player.draws, 0)

    def test_record_win(self):
        """Calling record_win should increase win count by one."""
        self.player.record_win()
        self.assertEqual(self.player.wins, 1)

    def test_record_loss(self):
        """Calling record_loss should increase loss count by one."""
        self.player.record_loss()
        self.assertEqual(self.player.losses, 1)

    def test_record_draw(self):
        """Calling record_draw should increase draw count by one."""
        self.player.record_draw()
        self.assertEqual(self.player.draws, 1)

    def test_reset_stats(self):
        """
        Calling reset_stats should set all stats to zero, regardless of current values.
        """
        self.player.record_win()
        self.player.record_loss()
        self.player.record_draw()
        self.player.reset_stats()
        self.assertEqual(self.player.wins, 0)
        self.assertEqual(self.player.losses, 0)
        self.assertEqual(self.player.draws, 0)

if __name__ == '__main__':
    unittest.main()
