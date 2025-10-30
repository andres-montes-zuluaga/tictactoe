# Copyright 2025 Andrés Montes Zuluaga
# Licensed under the Apache License, Version 2.0 (see LICENSE file)

"""
Artificial Intelligence (AI) module for the computer player in TicTacToe.

Provides AIPlayer classes for different difficulty levels (easy, medium, hard/minimax),
with support for move time limits. Each class implements the method to select
the next move given the current board state.
"""

import random
import time
from typing import Tuple, Optional, List
from src.logic import Board

class BaseAIPlayer:
    """
    Abstract base class for any computer AI player.

    Attributes:
        mark (str): The AI's mark ('X' or 'O').
        max_time (float): Maximum time in seconds per move, 0 disables the limit.

    Methods:
        choose_move(board: Board) -> Tuple[int, int]: Choose a move given board state.
    """
    def __init__(self, mark: str, max_time: float = 0.0):
        self.mark = mark
        self.max_time = max_time

    def choose_move(self, board: Board) -> Optional[Tuple[int, int]]:
        """Override in subclasses to return (row, col) of move."""
        raise NotImplementedError


class RandomAIPlayer(BaseAIPlayer):
    """
    AI (Easy): Chooses a random available move.
    """
    def choose_move(self, board: Board) -> Optional[Tuple[int, int]]:
        # Record start time for enforcing time limit
        start_time = time.time()
        
        # Collect all available moves on the board as (row, col) pairs
        available_moves = [
            (row, col)
            for row in range(board.size)
            for col in range(board.size)
            if board.is_valid_move(row, col)
        ]
        if not available_moves:
            return None
        
        # If there is a time limit, pause briefly to simulate "thinking"
        if self.max_time > 0:
            time_remaining = self.max_time - (time.time() - start_time)
            if time_remaining > 0:
                time.sleep(min(time_remaining, 0.2))
        
        # Return a randomly selected move
        return random.choice(available_moves)


class MediumAIPlayer(BaseAIPlayer):
    """
    AI (Medium): Blocks immediate threats and tries to win;
    otherwise chooses a random move.
    """
    def choose_move(self, board: Board) -> Optional[Tuple[int, int]]:
        start_time = time.time()
        opponent_mark = 'O' if self.mark == 'X' else 'X'

        # 1. Try to win: Check every cell—if placing our mark there results in a win, play there
        for row in range(board.size):
            for col in range(board.size):
                if board.is_valid_move(row, col):
                    board.grid[row][col] = self.mark
                    if board.check_winner() == self.mark:
                        board.grid[row][col] = ''  # Undo move for simulation
                        return (row, col)
                    board.grid[row][col] = ''  # Undo

        # 2. Block opponent: Try every cell—if placing opponent's mark gives them a win, block there
        for row in range(board.size):
            for col in range(board.size):
                if board.is_valid_move(row, col):
                    board.grid[row][col] = opponent_mark
                    if board.check_winner() == opponent_mark:
                        board.grid[row][col] = ''  # Undo
                        return (row, col)
                    board.grid[row][col] = ''  # Undo

        # 3. If no win or block is possible, just make a random move
        random_ai = RandomAIPlayer(self.mark, self.max_time)
        move = random_ai.choose_move(board)

        # Optionally respect time limit again before final move
        if self.max_time > 0:
            time_remaining = self.max_time - (time.time() - start_time)
            if time_remaining > 0:
                time.sleep(min(time_remaining, 0.2))
        return move


class HardAIPlayer(BaseAIPlayer):
    """
    AI (Hard): Uses minimax algorithm (with optional time limit).

    Plays optimally for unbeatable TicTacToe AI unless limited by max_time.
    """
    def choose_move(self, board: Board) -> Optional[Tuple[int, int]]:
        start_time = time.time()
        best_score = float('-inf')
        best_move = None

        # Iterate through every possible valid move and choose the one with the highest minimax score
        for row in range(board.size):
            for col in range(board.size):
                if board.is_valid_move(row, col):
                    board.grid[row][col] = self.mark
                    score = self.minimax(board, is_maximizing=False, start_time=start_time)
                    board.grid[row][col] = ''
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        return best_move

    def minimax(self, board: Board, is_maximizing: bool, start_time: float) -> int:
        # If time limit is set and exceeded, exit recursion with neutral outcome
        if self.max_time > 0 and (time.time() - start_time) > self.max_time:
            return 0  # Considered a draw if time is up

        winner = board.check_winner()
        if winner == self.mark:
            return 1
        elif winner is not None:
            return -1
        elif board.is_full():
            return 0

        # Select maximizing or minimizing branch based on whose turn it is
        if is_maximizing:
            best_score = float('-inf')
            current_mark = self.mark
        else:
            best_score = float('inf')
            current_mark = 'O' if self.mark == 'X' else 'X'

        for row in range(board.size):
            for col in range(board.size):
                if board.is_valid_move(row, col):
                    board.grid[row][col] = current_mark
                    score = self.minimax(board, not is_maximizing, start_time)
                    board.grid[row][col] = ''
                    
                    # Decide whether to maximize or minimize
                    if is_maximizing:
                        if score > best_score:
                            best_score = score
                    else:
                        if score < best_score:
                            best_score = score
        return best_score


def get_ai_player(level: str, mark: str, max_time: float = 0.0) -> BaseAIPlayer:
    """
    Factory function to create AI instance by difficulty.
    level: 'easy', 'medium', 'hard'
    """
    if level == "easy":
        return RandomAIPlayer(mark, max_time)
    elif level == "medium":
        return MediumAIPlayer(mark, max_time)
    elif level == "hard":
        return HardAIPlayer(mark, max_time)
    else:
        raise ValueError(f"Unknown AI level: {level}")
