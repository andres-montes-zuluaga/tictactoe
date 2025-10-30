# Copyright 2025 Andrés Montes Zuluaga
# Licensed under the Apache License, Version 2.0 (see LICENSE file)

"""
Player and score management for TicTacToe.

Handles persistent storage and retrieval of player names, wins, losses, draws and score records
using a JSON file in the data/ directory. Provides API for statistics management and lookups.
"""

import json
import os
from typing import Dict, Any

class ScoresManager:
    """
    Manages saving and loading player scores to a JSON file for persistence.

    Attributes:
        file_path (str): Path to the JSON file used for storage.

    Methods:
        load_scores() -> Dict: Loads all scores from file.
        save_scores(scores: Dict): Saves the scores dictionary to file.
        get_player_score(name: str) -> Dict: Returns stats for a player.
        update_player_score(name: str, result: str): Updates stats ('win', 'loss', 'draw').
        get_leaderboard(top_n: int = 5) -> List: Returns top N players by wins.
    """
    def __init__(self, file_path: str = 'data/scores.json'):
        self.file_path = file_path
        # Initialize the data file if it doesn't exist
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, 'w') as f:
                json.dump({}, f)

    def load_scores(self) -> Dict[str, Any]:
        """Loads all player scores from the JSON file."""
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def save_scores(self, scores: Dict[str, Any]) -> None:
        """Saves all player scores to the JSON file."""
        with open(self.file_path, 'w') as f:
            json.dump(scores, f, indent=2)

    def get_player_score(self, name: str) -> Dict[str, int]:
        """
        Returns the score dict for a player, or initializes it if not present.

        Returns:
            A dict with 'wins', 'losses', and 'draws'.
        """
        scores = self.load_scores()
        if name not in scores:
            scores[name] = {"wins": 0, "losses": 0, "draws": 0}
            self.save_scores(scores)
        return scores[name]

    def update_player_score(self, name: str, result: str) -> None:
        """
        Updates the score for a player based on result ('win', 'loss', 'draw').
        """
        scores = self.load_scores()
        if name not in scores:
            scores[name] = {"wins": 0, "losses": 0, "draws": 0}
        if result == "win":
            scores[name]["wins"] += 1
        elif result == "loss":
            scores[name]["losses"] += 1
        elif result == "draw":
            scores[name]["draws"] += 1
        self.save_scores(scores)

    def get_leaderboard(self, top_n: int = 5):
        """
        Returns a sorted list of top N players by number of wins (descending).
        """
        scores = self.load_scores()
        sorted_players = sorted(
            scores.items(),
            key=lambda item: item[1]["wins"],
            reverse=True
        )
        return sorted_players[:top_n]
