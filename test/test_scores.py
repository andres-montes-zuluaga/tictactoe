"""
Unit tests for ScoresManager in src.scores.

Verifies correct loading, saving, updating player stats,
and leaderboard sorting using a temporary test file.
"""

import unittest
import os
import json
from src.scores import ScoresManager

class TestScoresManager(unittest.TestCase):
    """Tests for the ScoresManager class."""

    def setUp(self):
        """
        Prepare: Use a temporary file so real game stats are not affected.
        Create a fresh ScoresManager for each run.
        """
        self.test_file = 'data/scores_test.json'
        # Ensure test file is clean
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.scores = ScoresManager(file_path=self.test_file)

    def tearDown(self):
        """Cleanup: Remove temp test file after each test run."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_initialization_creates_file(self):
        """ScoresManager should create a file on init if it doesn't exist."""
        self.assertTrue(os.path.exists(self.test_file))
        with open(self.test_file, 'r') as f:
            data = json.load(f)
            self.assertEqual(data, {})

    def test_update_and_get_player_score(self):
        """
        Updating a player's stats should persist wins/losses/draws.
        """
        self.scores.update_player_score("Bob", "win")
        self.scores.update_player_score("Bob", "loss")
        self.scores.update_player_score("Bob", "draw")
        stats = self.scores.get_player_score("Bob")
        self.assertEqual(stats["wins"], 1)
        self.assertEqual(stats["losses"], 1)
        self.assertEqual(stats["draws"], 1)

    def test_get_player_score_initializes_if_missing(self):
        """
        A new player should be created with stats at zero.
        """
        stats = self.scores.get_player_score("Charlie")
        self.assertEqual(stats, {"wins": 0, "losses": 0, "draws": 0})

    def test_leaderboard_returns_sorted_players(self):
        """
        Leaderboard should return players sorted by wins in descending order.
        """
        self.scores.update_player_score("Alice", "win")
        self.scores.update_player_score("Bob", "win")
        self.scores.update_player_score("Bob", "win")
        leaderboard = self.scores.get_leaderboard(top_n=2)
        self.assertEqual(leaderboard[0][0], "Bob")
        self.assertEqual(leaderboard[0][1]["wins"], 2)
        self.assertEqual(leaderboard[1][0], "Alice")
        self.assertEqual(leaderboard[1][1]["wins"], 1)

if __name__ == '__main__':
    unittest.main()
