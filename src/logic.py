# Copyright 2025 Andrés Montes Zuluaga
# Licensed under the Apache License, Version 2.0 (see LICENSE file)

"""
TicTacToe - Game Logic (Board)

Provides the Board class representing the game state and enforcing all rules.
Handles move validation, victory/draw checking, state mutation and reset.

Designed for modularity and easy integration with GUI and AI modules.

"""

from typing import List, Optional, Tuple

class Board:
    """
    The Board class encapsulates the state and logic for TicTacToe
    on a square (default 3x3) grid.

    - Tracks the grid, current turn, and move legality.
    - Exposes methods for move validation, victory/draw detection, and reset.
    - Used by both human and AI players via the GUI layer.
    """

    def __init__(self, size: int = 3):
        """
        Initializes the board and starting state.

        Args:
            size (int): The board/grid dimension (classic TicTacToe = 3)
        """
        self.size = size
        self.grid: List[List[str]] = [["" for _ in range(size)] for _ in range(size)]
        # 'X' always starts by tradition/convention
        self.turn: str = "X"

    def reset(self):
        """
        Clears the board and resets turn to 'X'.
        """
        self.grid = [["" for _ in range(self.size)] for _ in range(self.size)]
        self.turn = "X"

    def is_full(self) -> bool:
        """
        Returns True if the board is filled with marks (draw), False otherwise.
        """
        for row_cells in self.grid:
            for cell in row_cells:
                if cell == "":
                    return False
        return True

    def is_valid_move(self, row: int, col: int) -> bool:
        """
        Checks whether a move to (row, col) is legal/available.

        Returns:
            bool: True if square is empty and in bounds, False otherwise.
        """
        return (
            0 <= row < self.size
            and 0 <= col < self.size
            and self.grid[row][col] == ""
        )

    def make_move(self, row: int, col: int) -> bool:
        """
        Places the current player's mark in the specified cell if the move is valid.
        Automatically switches player turns if move is made.

        Args:
            row, col (int): The move location.

        Returns:
            bool: True if move was made, False if move was not legal.
        """
        if self.is_valid_move(row, col):
            self.grid[row][col] = self.turn
            # Switch turn after successful move
            self.turn = "O" if self.turn == "X" else "X"
            return True
        return False

    def check_winner(self) -> Optional[str]:
        """
        Checks current board for a winner ("X" or "O") or no winner yet (None).

        Returns:
            str or None: The mark ('X' or 'O') of the winning player, or None if
            there is no winner yet.
        """
        # Check rows and columns
        for idx in range(self.size):
            if (
                self.grid[idx][0] != ""
                and all(self.grid[idx][col] == self.grid[idx][0] for col in range(self.size))
            ):
                return self.grid[idx][0]
            if (
                self.grid[0][idx] != ""
                and all(self.grid[row][idx] == self.grid[0][idx] for row in range(self.size))
            ):
                return self.grid[0][idx]
        # Check diagonals
        if (
            self.grid[0][0] != ""
            and all(self.grid[i][i] == self.grid[0][0] for i in range(self.size))
        ):
            return self.grid[0][0]
        if (
            self.grid[0][self.size - 1] != ""
            and all(self.grid[i][self.size - 1 - i] == self.grid[0][self.size - 1] for i in range(self.size))
        ):
            return self.grid[0][self.size - 1]
        return None

    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """
        Returns a list of (row, col) tuples for all currently empty squares.
        Useful for AI move selection.
        """
        return [
            (row_idx, col_idx)
            for row_idx, row_cells in enumerate(self.grid)
            for col_idx, cell in enumerate(row_cells)
            if cell == ""
        ]

    # Optional: provide __str__ for debugging/printing
    def __str__(self):
        """
        Provides a string representation of the current board state.
        """
        rows = []
        for row in self.grid:
            rows.append(" | ".join(cell if cell != "" else " " for cell in row))
        return "\n" + "\n" + "-" * (self.size * 4 - 1) + "\n".join(rows) + "\n"

