import unittest
from src.logic import Board
from src.ai import get_ai_player

class TestAIPlayers(unittest.TestCase):
    """
    Unittest for AI decision-making (Random, Medium, Hard) via get_ai_player.
    Ensures AI proposes legal moves and can block/win appropriately.
    """

    def setUp(self):
        self.board = Board(size=3)

    def test_random_ai_move(self):
        ai = get_ai_player("easy", mark="O")
        move = ai.choose_move(self.board)
        self.assertIn(move, [(row, col) for row in range(3) for col in range(3)])

    def test_medium_ai_win(self):
        # O can win
        self.board.grid = [
            ["O", "O", ""],
            ["X", "X", ""],
            ["", "", ""]
        ]
        ai = get_ai_player("medium", mark="O")
        move = ai.choose_move(self.board)
        self.assertEqual(move, (0, 2))

    def test_medium_ai_block(self):
        # X can win, O should block
        self.board.grid = [
            ["X", "X", ""],
            ["O", "", ""],
            ["", "", ""]
        ]
        ai = get_ai_player("medium", mark="O")
        move = ai.choose_move(self.board)
        self.assertEqual(move, (0, 2))

    def test_hard_ai_minimax(self):
        # Use minimax: O must pick best move to block win and play optimally
        self.board.grid = [
            ["X", "X", ""],
            ["O", "", ""],
            ["", "", ""]
        ]
        ai = get_ai_player("hard", mark="O")
        move = ai.choose_move(self.board)
        self.assertEqual(move, (0, 2))

    def test_ai_respects_full_board(self):
        self.board.grid = [
            ["X", "O", "X"],
            ["X", "O", "O"],
            ["O", "X", "X"]
        ]
        ai = get_ai_player("easy", mark="O")
        move = ai.choose_move(self.board)
        self.assertIsNone(move)

if __name__ == "__main__":
    unittest.main()
