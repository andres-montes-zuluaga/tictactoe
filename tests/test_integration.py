import unittest
import os
import tempfile
from src.logic import Board
from src.ai import get_ai_player
from src.scores import ScoresManager

class TestTicTacToeIntegration(unittest.TestCase):
    """
    Integration test for full game logic:
    - Simulates playing a game between a human and AI
    - Checks moves, win detection, score updating and leaderboard
    """

    def setUp(self):
        # Temp file for testing scores without polluting real leaderboard
        fd, path = tempfile.mkstemp()
        os.close(fd)
        self.temp_file_path = path
        self.scores = ScoresManager(self.temp_file_path)
        self.board = Board(size=3)

    def tearDown(self):
        os.remove(self.temp_file_path)

    def test_human_vs_ai_play_and_score(self):
        # Names for players
        player_human = "TestHuman"
        player_ai = "TestBot"

        # Simulate: Human (X) in (0,0), AI (O) in (1,1), Human in (0,1), AI in (2,2), Human in (0,2) WIN
        self.assertTrue(self.board.make_move(0, 0))  # X
        ai = get_ai_player("easy", mark="O")
        move_ai_1 = ai.choose_move(self.board)
        self.assertTrue(self.board.make_move(*move_ai_1))  # O
        self.assertTrue(self.board.make_move(0, 1))  # X
        move_ai_2 = ai.choose_move(self.board)
        self.assertTrue(self.board.make_move(*move_ai_2))  # O
        self.assertTrue(self.board.make_move(0, 2))  # X now row 0 should be ['X', 'X', 'X'], human wins!

        winner = self.board.check_winner()
        self.assertEqual(winner, "X")

        # Update scores: X=win, O=loss
        self.scores.update_player_score(player_human, "win")
        self.scores.update_player_score(player_ai, "loss")

        score_human = self.scores.get_player_score(player_human)
        score_ai = self.scores.get_player_score(player_ai)
        self.assertEqual(score_human["games_won"], 1)
        self.assertEqual(score_human["games_played"], 1)
        self.assertEqual(score_ai["games_lost"], 1)
        self.assertEqual(score_ai["games_played"], 1)

        # Leaderboard should now put human ahead of bot
        leaderboard = self.scores.get_leaderboard(top_n=2)
        self.assertEqual(leaderboard[0]["name"], player_human)

    def test_full_draw_and_score_update(self):
        # Names
        player_X = "Alice"
        player_O = "Bob"
        # Fill grid to draw (no winner possible)
        moves = [(0,0),(0,1),(0,2),(1,1),(1,0),(1,2),(2,1),(2,0),(2,2)]
        marks = ["X", "O"] * 5
        for i, (row, col) in enumerate(moves):
            self.board.grid[row][col] = marks[i]
        self.assertIsNone(self.board.check_winner())
        self.assertTrue(self.board.is_full())

        self.scores.update_player_score(player_X, "draw")
        self.scores.update_player_score(player_O, "draw")

        score_x = self.scores.get_player_score(player_X)
        score_o = self.scores.get_player_score(player_O)

        self.assertEqual(score_x["games_drawn"], 1)
        self.assertEqual(score_o["games_drawn"], 1)
        self.assertEqual(score_x["games_played"], 1)
        self.assertEqual(score_o["games_played"], 1)

if __name__ == "__main__":
    unittest.main()
