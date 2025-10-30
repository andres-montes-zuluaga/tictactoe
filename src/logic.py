# Copyright 2025 Andrés Montes Zuluaga
# Licensed under the Apache License, Version 2.0 (see LICENSE file)

"""
Core game logic and rules for TicTacToe.

This module defines classes that encapsulate the board, player management,
move validation, turn switching, win/draw detection, and board reset functionality.
"""

from typing import List, Optional, Tuple

class Board:
    """
    Represents the TicTacToe game board and provides game rule methods.

    Attributes:
        size (int): Board size (typically 3 for standard TicTacToe).
        grid (List[List[str]]): 2D array holding board state: 'X', 'O', or ''.

    Methods:
        reset(): Clears the board for a new game.
        make_move(row: int, col: int, mark: str) -> bool: Attempts to place a mark.
        is_valid_move(row: int, col: int) -> bool: Checks if a cell is free.
        check_winner() -> Optional[str]: Checks board for a winner ('X' or 'O').
        is_full() -> bool: Returns True if the board is full.
        check_draw() -> bool: Returns True if the game is a draw.
    """
    def __init__(self, size: int = 3):
        self.size = size
        self.grid = [['' for _ in range(size)] for _ in range(size)]

    def reset(self):
        """Resets the board to the empty state."""
        self.grid = [['' for _ in range(self.size)] for _ in range(self.size)]

    def make_move(self, row: int, col: int, mark: str) -> bool:
        """Attempts to place a mark ('X' or 'O') at the specified cell."""
        if self.is_valid_move(row, col):
            self.grid[row][col] = mark
            return True
        return False

    def is_valid_move(self, row: int, col: int) -> bool:
        """Checks if the specified cell is free for a move."""
        return 0 <= row < self.size and 0 <= col < self.size and self.grid[row][col] == ''

    def check_winner(self) -> Optional[str]:
        """Checks for a winning condition. Returns 'X', 'O', or None."""
        # Check rows and columns
        for i in range(self.size):
            if self.grid[i][0] != '' and all(self.grid[i][j] == self.grid[i][0] for j in range(self.size)):
                return self.grid[i][0]
            if self.grid[0][i] != '' and all(self.grid[j][i] == self.grid[0][i] for j in range(self.size)):
                return self.grid[0][i]
        # Check diagonals
        if self.grid[0][0] != '' and all(self.grid[i][i] == self.grid[0][0] for i in range(self.size)):
            return self.grid[0][0]
        if self.grid[0][self.size - 1] != '' and all(self.grid[i][self.size - 1 - i] == self.grid[0][self.size - 1] for i in range(self.size)):
            return self.grid[0][self.size - 1]
        return None

    def is_full(self) -> bool:
        """Returns True if the board is full."""
        return all(cell != '' for row in self.grid for cell in row)

    def check_draw(self) -> bool:
        """Returns True if the board is full and there is no winner."""
        return self.is_full() and self.check_winner() is None


class Player:
    """
    Represents a TicTacToe player.

    Attributes:
        name (str): Player name.
        mark (str): Player's mark ('X' or 'O').
        wins (int): Number of games won.
        losses (int): Number of games lost.
        draws (int): Number of draws.

    Methods:
        record_win(): Increases win count.
        record_loss(): Increases loss count.
        record_draw(): Increases draw count.
        reset_stats(): Resets stats for this player.
    """
    def __init__(self, name: str, mark: str):
        self.name = name
        self.mark = mark
        self.wins = 0
        self.losses = 0
        self.draws = 0

    def record_win(self):
        self.wins += 1

    def record_loss(self):
        self.losses += 1

    def record_draw(self):
        self.draws += 1

    def reset_stats(self):
        self.wins = 0
        self.losses = 0
        self.draws = 0
