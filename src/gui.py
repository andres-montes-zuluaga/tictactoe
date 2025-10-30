# Copyright 2025 Andrés Montes Zuluaga
# Licensed under the Apache License, Version 2.0 (see LICENSE file)

"""
Graphical User Interface (GUI) for TicTacToe using pygame.

Handles main menu, player name input, displaying the board, buttons, messages,
and visual feedback. Connects user actions to game logic and updates the display.
"""

import pygame

class GameGUI:
    """
    Main GUI controller for the TicTacToe game.

    Attributes:
        screen (pygame.Surface): Main window surface.
        width (int): Window width.
        height (int): Window height.
        running (bool): Controls main loop.
        state (str): Current screen state ('menu', 'play', 'stats', etc.).

    Methods:
        run(): Starts pygame GUI loop.
        draw_menu(): Draws the main menu.
        draw_board(board): Draws the game board state.
        draw_player_inputs(): Handles and draws name input boxes.
        draw_scores(scores): Displays player statistics.
        handle_events(): Dispatches pygame events and updates game state.
        show_message(text): Displays popup or temporary feedback.
    """
    def __init__(self, width: int = 600, height: int = 600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("TicTacToe")
        self.running = True
        self.state = 'menu'
        self.font = pygame.font.SysFont('Arial', 32)
        # Additional GUI elements can be initialized here

    def run(self):
        """
        Main loop for handling GUI updates and events.
        Keeps running until window is closed or game ends.
        """
        while self.running:
            self.handle_events()
            self.screen.fill((240, 240, 240))  # Background color

            if self.state == 'menu':
                self.draw_menu()
            elif self.state == 'play':
                # You'd pass the current board state here
                pass
            elif self.state == 'scores':
                pass
            pygame.display.flip()

    def draw_menu(self):
        """
        Displays main menu with buttons for starting game, viewing statistics, quitting, etc.
        """
        title_text = self.font.render("TicTacToe", True, (0, 0, 0))
        self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 100))
        # Draw buttons here (Start, Stats, Quit...)
        # Use pygame.draw.rect and pygame.font.render for visuals

    def draw_board(self, board):
        """
        Draws the tic-tac-toe board and current game state.
        Receives a Board instance to visualize marks and grid.
        """
        grid_size = min(self.width, self.height) * 0.6
        margin = (self.width - grid_size) // 2
        cell_size = grid_size // board.size
        for row in range(board.size):
            for col in range(board.size):
                x = margin + col * cell_size
                y = margin + row * cell_size
                pygame.draw.rect(self.screen, (200, 200, 200), (x, y, cell_size, cell_size), 3)
                mark = board.grid[row][col]
                if mark:
                    mark_text = self.font.render(mark, True, (0, 0, 0))
                    self.screen.blit(mark_text, (
                        x + cell_size // 2 - mark_text.get_width() // 2,
                        y + cell_size // 2 - mark_text.get_height() // 2
                    ))

    def draw_player_inputs(self):
        """
        Displays input boxes or instructions to enter player names before starting.
        """
        # Implement pygame input fields or simple text entry

    def draw_scores(self, scores):
        """
        Displays saved statistics and leaderboards.
        """
        # Draw scores and rankings, fetched from ScoresManager

    def handle_events(self):
        """
        Processes user input: mouse clicks, key presses, window events.
        Updates state and dispatches actions.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # Handle button clicks, keypresses, board clicks, etc.

    def show_message(self, text):
        """
        Displays a temporary message or popup for feedback.
        """
        message = self.font.render(text, True, (255, 0, 0))
        self.screen.blit(message, (self.width // 2 - message.get_width() // 2, self.height // 2))

