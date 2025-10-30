# Copyright 2025 Andrés Montes Zuluaga
# Licensed under the Apache License, Version 2.0 (see LICENSE file)

"""
TicTacToe - Scores Management

Provides the ScoresManager class for managing persistent player statistics
in TicTacToe. Stores win/loss/draw counts and games played for each player.
Handles reading and writing stats to a JSON file (data/scores.json) and
provides lookup and leaderboard utilities.

"""

import json
import os
from typing import Dict, Any, List, Tuple

class ScoresManager:
    """
    Responsible for saving and loading player scores for persistent statistics.

    - Creates/initializes the data file on first use.
    - Provides methods for score lookup, modification, and leaderboard retrieval.

    Attributes:
        file_path (str): Path to JSON file for scores.
    """

    def __init__(self, file_path: str = 'data/scores.json'):
        self.file_path = file_path
        # Create file & dirs if not present, and make sure it's always a list of dicts for compatibility with leaderboard screens
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)  # initialize with empty list (not dict)

    def load_scores(self) -> List[Dict[str, Any]]:
        """
        Loads the full list of player records from JSON file.

        Returns:
            List[Dict]: List of score dicts (name, games_played, games_won, games_lost, games_drawn)
        """
        with open(self.file_path, 'r', encoding='utf-8') as f:
            try:
                scores = json.load(f)
            except Exception:
                scores = []
        return scores

    def save_scores(self, scores: List[Dict[str, Any]]) -> None:
        """
        Saves the full list of player records to JSON.
        """
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(scores, f, indent=2)

    def get_player_score(self, name: str) -> Dict[str, Any]:
        """
        Returns or initializes the score record for a player, by name.

        Returns:
            Dict with fields: name, games_played, games_won, games_lost, games_drawn
        """
        scores = self.load_scores()
        for player in scores:
            if player["name"] == name:
                return player
        # Not found, initialize
        new_record = {
            "name": name,
            "games_played": 0,
            "games_won": 0,
            "games_lost": 0,
            "games_drawn": 0
        }
        scores.append(new_record)
        self.save_scores(scores)
        return new_record

    def update_player_score(self, name: str, result: str) -> None:
        """
        Updates the player's statistic based on game outcome.

        Args:
            name (str): Player name.
            result (str): "win", "loss", or "draw"
        """
        scores = self.load_scores()
        found = False
        for player in scores:
            if player["name"] == name:
                found = True
                player["games_played"] += 1
                if result == "win":
                    player["games_won"] += 1
                elif result == "loss":
                    player["games_lost"] += 1
                elif result == "draw":
                    player["games_drawn"] += 1
                break
        if not found:
            # Initialize new record if user never played before
            new_record = {
                "name": name,
                "games_played": 1,
                "games_won": 1 if result == "win" else 0,
                "games_lost": 1 if result == "loss" else 0,
                "games_drawn": 1 if result == "draw" else 0
            }
            scores.append(new_record)
        self.save_scores(scores)

    def get_leaderboard(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """
        Returns a sorted list of the top N players by number of games won, for leaderboard screen.

        Args:
            top_n (int): Number of top players to return.

        Returns:
            List[Dict]: Sorted list of player score dicts.
        """
        scores = self.load_scores()
        sorted_players = sorted(
            scores,
            key=lambda player: player["games_won"],
            reverse=True
        )
        return sorted_players[:top_n]

    def get_all_scores(self) -> List[Dict[str, Any]]:
        """
        Returns all player scores, unsorted (for full stats table).
        """
        return self.load_scores()

