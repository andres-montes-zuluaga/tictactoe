"""
Unit tests for AI players in src.ai.

Tests whether each AI player chooses moves correctly and within game constraints.
"""

import unittest
from src.logic import Board
from src.ai import get_ai_player, RandomAIPlayer, MediumAIPlayer, HardAIPlayer

class TestAIPlayers(unittest.TestCase):
    """Tests for AI player move selection."""

    def setUp(self):
        """Creates a fresh board before each test."""
        self.board = Board()
        self.board.reset()

    def test_random_ai_moves_are_valid(self):
        """
        RandomAIPlayer should always pick an empty cell.
        """
        ai_player = RandomAIPlayer('X')
        move = ai_player.choose_move(self.board)
        self.assertIsNotNone(move)
        row, col = move
        self.assertTrue(self.board.is_valid_move(row, col))

    def test_medium_ai_blocks_or_wins(self):
        """
        MediumAIPlayer should block opponent's win or win if possible.
        """
        ai_player = MediumAIPlayer('X')
        # Scenario: opponent 'O' is about to win, AI should block
        self.board.grid = [
            ['O', 'O', ''],
            ['X', '', ''],
            ['', '', '']
        ]
        move = ai_player.choose_move(self.board)
        self.assertEqual(move, (0, 2))  # AI should block opponent at (0,2)

        # Scenario: AI can win
        self.board.grid = [
            ['X', 'X', ''],
            ['O', '', 'O'],
            ['', '', '']
        ]
        move = ai_player.choose_move(self.board)
        self.assertEqual(move, (0, 2))  # AI should win at (0,2)

    def test_hard_ai_plays_optimal(self):
        """
        HardAIPlayer should always select a winning or drawing move if possible.
        """
        ai_player = HardAIPlayer('X')
        # Set up a winnable board for 'X'
        self.board.grid = [
            ['X', 'O', 'X'],
            ['O', 'X', ''],
            ['', '', 'O']
        ]
        move = ai_player.choose_move(self.board)
        # In this classic final, 'X' should win by playing (2,0)
        self.assertEqual(move, (2, 0))
        # HardAI should never return an invalid move
        row, col = move
        self.assertTrue(self.board.is_valid_move(row, col))

    def test_factory_returns_correct_class(self):
        """
        get_ai_player should instantiate correct AI class based on difficulty.
        """
        easy_ai = get_ai_player('easy', 'X')
        self.assertIsInstance(easy_ai, RandomAIPlayer)
        med_ai = get_ai_player('medium', 'O')
        self.assertIsInstance(med_ai, MediumAIPlayer)
        hard_ai = get_ai_player('hard', 'X')
        self.assertIsInstance(hard_ai, HardAIPlayer)

if __name__ == '__main__':
    unittest.main()
