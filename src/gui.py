# Copyright 2025 Andrés Montes Zuluaga
# Licensed under the Apache License, Version 2.0 (see LICENSE file)

"""
TicTacToe - GUI Module

Provides the graphical user interface for the TicTacToe game, including menus,
player input, leaderboard, AI difficulty selection, and a playable board.
All game rule logic is delegated to the Board class (logic.py),
and all AI decision making is delegated to the AIPlayer classes (ai.py).

"""

import pygame
import sys
import json
import os
from src.ai import get_ai_player
from src.scores import ScoresManager

class GameGUI:
    """
    The graphical user interface controller for TicTacToe.
    Handles all user input, draws all screens, and delegates moves and validation
    to Board and AIPlayer as appropriate.

    Args:
        board (Board): Game board logic object.
        ai (BaseAIPlayer): AI logic object (Easy/Medium/Hard), updatable at runtime.
        width (int): Window width.
        height (int): Window height.
    """

    def __init__(self, board, ai, width=600, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("TicTacToe")
        self.running = True
        self.state = 'menu'
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 32)
        self.input_font = pygame.font.SysFont('Arial', 28)
        self.ticks = 0  # Used for blinking cursors

        # Game logic (injected)
        self.board = board
        self.ai = ai
        self.ai_level = "easy"  # Track current chosen level for GUI

        # Menu/UI state/controls
        self.buttons = [
            ("1 Vs. 1", 200),
            ("Play vs Machine", 270),
            ("View Statistics", 340),
            ("Quit", 410)
        ]
        self.player_names = ["", ""]
        self.input_rects = [
            pygame.Rect(220, 185, 240, 42),
            pygame.Rect(220, 265, 240, 42)
        ]
        self.active_input = 0
        self.continue_rect = None
        self.back_rect = None
        self.machine_name = ""
        self.machine_input_rect = pygame.Rect(220, 220, 240, 42)
        self.machine_active = True
        self.levels = [("Easy", 300, 'easy'), ("Medium", 360, 'medium'), ("Epic!", 420, 'hard')]
        self.level_selected = 0

        # State for game play
        self.show_board_names = ["", ""]
        self.play_mode = None  # 'human' or 'ai'
        self.board_message = ""
        
        # Scores manager
        self.scores_manager = ScoresManager()  # Use default path data/scores.json

    def run(self):
        """
        Main loop for GUI; keeps processing events and updating display until user quits.
        """
        while self.running:
            self.handle_events()
            self.screen.fill((230, 230, 250))
            if self.state == 'menu':
                self.draw_menu()
            elif self.state == 'player_input':
                self.draw_player_input()
            elif self.state == 'scores':
                self.draw_scores()
            elif self.state == 'vs_machine':
                self.draw_vs_machine()
            elif self.state == 'board':
                self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)
            self.ticks += 1
        pygame.quit()
        sys.exit()

    ### DRAWING AND UI METHODS ###

    def draw_menu(self):
        """
        Draws the main menu and handles button hover states.
        """
        title_font = pygame.font.SysFont('Arial', 52, bold=True)
        title_surface = title_font.render("TicTacToe", True, (30, 30, 88))
        self.screen.blit(title_surface, (self.width // 2 - title_surface.get_width() // 2, 80))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i, (text, y_pos) in enumerate(self.buttons):
            hovered = self.is_mouse_over_rect(
                mouse_x, mouse_y,
                pygame.Rect(self.width // 2 - 120, y_pos - 27, 240, 54)
            )
            self.draw_button(text, self.width // 2, y_pos, hovered=hovered)

    def draw_player_input(self):
        """
        Draws fields for user name input and navigation buttons. Shows a blinking cursor in the active input box.
        """
        self.screen.fill((245, 248, 255))
        font_title = pygame.font.SysFont('Arial', 40, bold=True)
        font_label = pygame.font.SysFont('Arial', 28)
        title_surface = font_title.render("Enter Player Names", True, (30, 30, 80))
        self.screen.blit(title_surface, (self.width // 2 - title_surface.get_width() // 2, 85))
        for idx, label in enumerate(("Player 1", "Player 2")):
            self.screen.blit(font_label.render(label + ":", True, (50, 50, 100)), (120, 192 + idx * 80))
            pygame.draw.rect(self.screen, (255, 255, 255), self.input_rects[idx], border_radius=8)
            pygame.draw.rect(self.screen, (90, 120, 170), self.input_rects[idx], width=2, border_radius=8)
            name_surface = self.input_font.render(self.player_names[idx], True, (30, 30, 35))
            self.screen.blit(name_surface, (self.input_rects[idx].x + 10, self.input_rects[idx].y + 7))
            if self.active_input == idx and (self.ticks // 30) % 2 == 0:
                cx = self.input_rects[idx].x + 10 + name_surface.get_width() + 2
                cy = self.input_rects[idx].y + 6
                pygame.draw.line(self.screen, (44, 44, 124), (cx, cy), (cx, cy + 26), 2)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        continue_rect = pygame.Rect(self.width // 2 - 110, 370, 220, 54)
        hovered_continue = self.is_mouse_over_rect(mouse_x, mouse_y, continue_rect)
        self.draw_button("Continue", self.width // 2, 397, hovered=hovered_continue)
        self.continue_rect = continue_rect
        back_rect = pygame.Rect(40, self.height - 70, 160, 44)
        hovered_back = self.is_mouse_over_rect(mouse_x, mouse_y, back_rect)
        self.draw_button("Back to Menu", 40 + 80, self.height - 48, hovered=hovered_back, width=160)
        self.back_rect = back_rect

    def draw_scores(self):
        """
        Loads score data and draws leaderboard table and return-to-menu button.
        """
        self.screen.fill((245, 245, 238))
        header_font = pygame.font.SysFont('Arial', 40, bold=True)
        font = pygame.font.SysFont('Arial', 22)
        title = header_font.render("Leaderboard", True, (80, 60, 25))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 45))
        path = os.path.join("data", "scores.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                scores = json.load(f)
        except Exception:
            scores = []
        labels = ["Name", "Played", "Won", "Lost", "Drawn"]
        for i, label in enumerate(labels):
            self.screen.blit(font.render(label, True, (80, 80, 60)), (55 + i * 100, 110))
        for idx, player in enumerate(scores):
            y = 140 + idx * 32
            self.screen.blit(font.render(player["name"], True, (40, 40, 20)), (55, y))
            self.screen.blit(font.render(str(player["games_played"]), True, (40, 40, 20)), (155, y))
            self.screen.blit(font.render(str(player["games_won"]), True, (40, 40, 20)), (255, y))
            self.screen.blit(font.render(str(player["games_lost"]), True, (40, 40, 20)), (355, y))
            self.screen.blit(font.render(str(player["games_drawn"]), True, (40, 40, 20)), (455, y))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        back_rect = pygame.Rect(self.width // 2 - 100, self.height - 60, 200, 48)
        hovered_back = self.is_mouse_over_rect(mouse_x, mouse_y, back_rect)
        self.draw_button("Back to Menu", self.width // 2, self.height - 36, hovered=hovered_back, width=200)
        self.back_rect = back_rect

    def draw_vs_machine(self):
        """
        Shows name input and AI level selection, plus navigation buttons. Updates AI on difficulty change.
        """
        self.screen.fill((244, 249, 252))
        font_title = pygame.font.SysFont('Arial', 40, bold=True)
        font_label = pygame.font.SysFont('Arial', 28)
        title_surface = font_title.render("Play vs Machine", True, (30, 30, 75))
        self.screen.blit(title_surface, (self.width // 2 - title_surface.get_width() // 2, 65))
        self.screen.blit(font_label.render("Your Name:", True, (50, 50, 100)), (110, 228))
        pygame.draw.rect(self.screen, (255, 255, 255), self.machine_input_rect, border_radius=8)
        pygame.draw.rect(self.screen, (90, 120, 170), self.machine_input_rect, width=2, border_radius=8)
        name_surface = self.input_font.render(self.machine_name, True, (30, 30, 35))
        self.screen.blit(name_surface, (self.machine_input_rect.x + 10, self.machine_input_rect.y + 7))
        if self.machine_active and (self.ticks // 30) % 2 == 0:
            cx = self.machine_input_rect.x + 10 + name_surface.get_width() + 2
            cy = self.machine_input_rect.y + 6
            pygame.draw.line(self.screen, (44, 44, 124), (cx, cy), (cx, cy + 26), 2)
        self.level_rects = []
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i, (level, y, internal_level) in enumerate(self.levels):
            rect = pygame.Rect(self.width // 2 - 80, y-22, 160, 44)
            hovered = self.is_mouse_over_rect(mouse_x, mouse_y, rect)
            selected = (i == self.level_selected)
            self.draw_button(
                level,
                self.width // 2, y,
                hovered=hovered or selected,
                width=160,
                color_active=(139, 220, 160) if selected else None
            )
            self.level_rects.append(rect)
        back_rect = pygame.Rect(38, self.height - 68, 164, 44)
        hovered_back = self.is_mouse_over_rect(mouse_x, mouse_y, back_rect)
        self.draw_button("Back to Menu", 38+82, self.height - 46, hovered=hovered_back, width=164)
        self.back_rect = back_rect
        continue_rect = pygame.Rect(self.width // 2 - 80, self.height - 100, 160, 44)
        hovered_continue = self.is_mouse_over_rect(mouse_x, mouse_y, continue_rect)
        self.draw_button("Continue", self.width // 2, self.height - 78, hovered=hovered_continue, width=160)
        self.continue_rect = continue_rect

    def draw_board(self):
        """
        Draws the playable board. Uses Board and AI logic for state and moves.
        Displays victory/draw message and allows returning to the menu.
        """
        self.screen.fill((240, 245, 255))
        font_title = pygame.font.SysFont('Arial', 36, bold=True)
        p1, p2 = self.show_board_names
        title = font_title.render(f"{p1} (X) vs {p2} (O)", True, (54, 43, 99))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 50))
        turn_font = pygame.font.SysFont('Arial', 24)
        turn_label = turn_font.render(f"Turn: {self.board.turn}", True, (55, 90, 120))
        self.screen.blit(turn_label, (self.width // 2 - turn_label.get_width() // 2, 100))
        if self.board_message:
            msg_font = pygame.font.SysFont('Arial', 30, bold=True)
            msg_surface = msg_font.render(self.board_message, True, (150, 40, 50))
            self.screen.blit(msg_surface, (self.width // 2 - msg_surface.get_width() // 2, 140))
        grid_size = min(self.width, self.height) * 0.6
        margin = (self.width - grid_size) // 2
        cell_size = grid_size // self.board.size
        self.square_rects = []
        for row in range(self.board.size):
            for col in range(self.board.size):
                x = int(margin + col * cell_size)
                y = int(160 + row * cell_size)
                rect = pygame.Rect(x, y, int(cell_size), int(cell_size))
                self.square_rects.append((rect, row, col))
                pygame.draw.rect(self.screen, (210, 210, 230), rect, border_radius=10)
                pygame.draw.rect(self.screen, (60, 80, 135), rect, width=3, border_radius=10)
                mark = self.board.grid[row][col]
                if mark:
                    mark_font = pygame.font.SysFont('Arial', 54, bold=True)
                    color = (30, 140, 70) if mark == "X" else (160, 55, 68)
                    mark_surface = mark_font.render(mark, True, color)
                    self.screen.blit(
                        mark_surface,
                        (x + cell_size//2 - mark_surface.get_width()//2,
                         y + cell_size//2 - mark_surface.get_height()//2)
                    )
        mouse_x, mouse_y = pygame.mouse.get_pos()
        back_rect = pygame.Rect(40, self.height - 70, 160, 44)
        hovered_back = self.is_mouse_over_rect(mouse_x, mouse_y, back_rect)
        self.draw_button("Back to Menu", 40+80, self.height - 48, hovered=hovered_back, width=160)
        self.back_rect = back_rect

    ### BUTTON, CURSOR AND EVENT HELPERS ###

    def draw_button(self, text, center_x, center_y, hovered=False, width=240, color_active=None):
        """
        Draws a button with optional hover and custom color effect.
        """
        rect_width, rect_height = width, 54
        button_rect = pygame.Rect(center_x - rect_width // 2, center_y - rect_height // 2, rect_width, rect_height)
        font = pygame.font.SysFont('Arial', 32)
        text_surface = font.render(text, True, (20, 20, 40))
        if hovered:
            color_fill = color_active if color_active else (140, 170, 255)
            border_color = (0, 64, 224)
            border_width = 4
            glow_color = (100, 140, 255)
            glow_rect = button_rect.inflate(10, 10)
            pygame.draw.rect(self.screen, glow_color, glow_rect, border_radius=16)
        else:
            color_fill = color_active if color_active else (185, 200, 235)
            border_color = (80, 80, 140)
            border_width = 2
        pygame.draw.rect(self.screen, color_fill, button_rect, border_radius=12)
        pygame.draw.rect(self.screen, border_color, button_rect, width=border_width, border_radius=12)
        self.screen.blit(
            text_surface,
            (center_x - text_surface.get_width() // 2, center_y - text_surface.get_height() // 2)
        )

    def is_mouse_over_rect(self, mouse_x, mouse_y, rect):
        """
        Returns True if mouse is over the given rectangle area.
        """
        return rect.collidepoint(mouse_x, mouse_y)

    def reset_game(self):
        """
        Resets the board and message for a new game session.
        """
        self.board.reset()
        self.board_message = ""

    ### MAIN EVENT HANDLING AND GAME FLOW ###

    def handle_events(self):
        """
        Processes all events - mouse and keyboard.
        Delegates to Board and AI for move validation and turn processing.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif self.state == 'menu':
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = event.pos
                    for i, (text, y_pos) in enumerate(self.buttons):
                        rect = pygame.Rect(self.width // 2 - 120, y_pos - 27, 240, 54)
                        if rect.collidepoint(mouse_x, mouse_y):
                            if text == "1 Vs. 1":
                                self.player_names = ["", ""]
                                self.active_input = 0
                                self.state = 'player_input'
                                self.play_mode = 'human'
                            elif text == "Play vs Machine":
                                self.machine_name = ""
                                self.machine_active = True
                                self.state = 'vs_machine'
                                self.play_mode = 'ai'
                            elif text == "View Statistics":
                                self.state = 'scores'
                            elif text == "Quit":
                                self.running = False

            elif self.state == 'player_input':
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    for idx, rect in enumerate(self.input_rects):
                        if rect.collidepoint(mx, my):
                            self.active_input = idx
                            break
                    else:
                        self.active_input = None
                    if self.continue_rect and self.continue_rect.collidepoint(mx, my):
                        if all(n.strip() != "" for n in self.player_names):
                            self.show_board_names = [self.player_names[0], self.player_names[1]]
                            self.reset_game()
                            self.state = 'board'
                    if self.back_rect and self.back_rect.collidepoint(mx, my):
                        self.state = 'menu'
                elif event.type == pygame.KEYDOWN and self.active_input is not None:
                    if event.key == pygame.K_BACKSPACE:
                        self.player_names[self.active_input] = self.player_names[self.active_input][:-1]
                    elif event.key in (pygame.K_TAB, pygame.K_DOWN):
                        self.active_input = (self.active_input + 1) % 2
                    elif event.key == pygame.K_UP:
                        self.active_input = (self.active_input - 1) % 2
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        self.active_input = None
                    else:
                        char = event.unicode
                        if len(self.player_names[self.active_input]) < 12 and char.isprintable():
                            self.player_names[self.active_input] += char

            elif self.state == 'scores':
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    if self.back_rect and self.back_rect.collidepoint(mx, my):
                        self.state = 'menu'

            elif self.state == 'vs_machine':
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    if self.machine_input_rect.collidepoint(mx, my):
                        self.machine_active = True
                    else:
                        self.machine_active = False
                    # AI level selection - update the AI dynamically
                    for i, rect in enumerate(self.level_rects):
                        if rect.collidepoint(mx, my):
                            self.level_selected = i
                            selected_level_str = self.levels[i][2]  # 'easy', 'medium', 'hard'
                            self.ai_level = selected_level_str
                            self.ai = get_ai_player(level=self.ai_level, mark="O", max_time=1.0)
                    # Continue to game if name was entered
                    if self.continue_rect and self.continue_rect.collidepoint(mx, my):
                        if self.machine_name.strip() != "":
                            self.show_board_names = [self.machine_name, f"Bot ({self.levels[self.level_selected][0]})"]
                            self.reset_game()
                            self.state = 'board'
                    if self.back_rect and self.back_rect.collidepoint(mx, my):
                        self.state = 'menu'
                elif event.type == pygame.KEYDOWN and self.machine_active:
                    if event.key == pygame.K_BACKSPACE:
                        self.machine_name = self.machine_name[:-1]
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        self.machine_active = False
                    else:
                        char = event.unicode
                        if len(self.machine_name) < 12 and char.isprintable():
                            self.machine_name += char

            elif self.state == 'board':
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    # Handle human move, then possibly AI move
                    for rect, row, col in self.square_rects:
                        if rect.collidepoint(mx, my):
                            if self.board.grid[row][col] == "" and not self.board_message:
                                # Player move
                                move_done = self.board.make_move(row, col)
                                if move_done:
                                    winner = self.board.check_winner()
                                    if winner:
                                        self.board_message = f"{winner} wins!"
                                        # Update scores
                                        self.scores_manager.update_player_score(self.show_board_names[0 if winner == "X" else 1], "win")
                                        self.scores_manager.update_player_score(self.show_board_names[1 if winner == "X" else 0], "loss")
                                    elif self.board.is_full():
                                        self.board_message = "Draw!"
                                        self.scores_manager.update_player_score(self.show_board_names[0], "draw")
                                        self.scores_manager.update_player_score(self.show_board_names[1], "draw")
                                    # Handle AI response if appropriate
                                    if self.play_mode == 'ai' and self.board.turn == "O" and not self.board_message:
                                        move = self.ai.choose_move(self.board)
                                        if move is not None:
                                            ai_row, ai_col = move
                                            self.board.make_move(ai_row, ai_col)
                                            winner = self.board.check_winner()
                                            if winner:
                                                self.board_message = f"{winner} wins!"
                                            elif self.board.is_full():
                                                self.board_message = "Draw!"
                    if self.back_rect and self.back_rect.collidepoint(mx, my):
                        self.reset_game()
                        self.state = 'menu'

if __name__ == "__main__":
    print("Please run the game using main.py at the project root.")
