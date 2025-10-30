import unittest
import os
import tempfile
from src.scores import ScoresManager

class TestScoresManager(unittest.TestCase):
    """
    Unittest for ScoresManager score tracking and persistence logic.
    """

    def setUp(self):
        # Use a temp file to avoid polluting real leaderboard
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.manager = ScoresManager(self.temp_file.name)

    def tearDown(self):
        # Clean up temp file
        os.remove(self.temp_file.name)

    def test_initialize_and_get_player(self):
        score = self.manager.get_player_score("Alice")
        self.assertEqual(score["name"], "Alice")
        self.assertEqual(score["games_won"], 0)
        self.assertEqual(score["games_lost"], 0)
        self.assertEqual(score["games_drawn"], 0)
        self.assertEqual(score["games_played"], 0)

    def test_update_win_loss_draw(self):
        self.manager.update_player_score("Bob", "win")
        self.manager.update_player_score("Bob", "loss")
        self.manager.update_player_score("Bob", "draw")
        score = self.manager.get_player_score("Bob")
        self.assertEqual(score["games_played"], 3)
        self.assertEqual(score["games_won"], 1)
        self.assertEqual(score["games_lost"], 1)
        self.assertEqual(score["games_drawn"], 1)

    def test_leaderboard_sorting(self):
        self.manager.update_player_score("Cleo", "win")
        self.manager.update_player_score("Cleo", "win")
        self.manager.update_player_score("Dan", "win")
        self.manager.update_player_score("Bob", "loss")
        top_players = self.manager.get_leaderboard(top_n=2)
        self.assertEqual(top_players[0]["name"], "Cleo")
        self.assertEqual(top_players[1]["name"], "Dan")

    def test_persistence_between_loads(self):
        self.manager.update_player_score("Elena", "win")
        manager2 = ScoresManager(self.temp_file.name)
        score2 = manager2.get_player_score("Elena")
        self.assertEqual(score2["games_won"], 1)
        self.assertEqual(score2["games_played"], 1)

if __name__ == "__main__":
    unittest.main()
