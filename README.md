# TicTacToe Game (Python + Pygame)

A modular implementation of the classic game TicTacToe with a graphical user interface, AI player logic at three difficulty levels, persistent scoreboard, and comprehensive tests.

## Features

- Modern GUI built with Pygame: menu, player name input, game board, leaderboard and more.
- Flexible opponent modes: Human vs Human, Human vs Computer (Easy, Medium, Epic/Hard).
- Advanced AI strategies: random, blocking/winning, unbeatable minimax.
- Persistent player statistics with wins, losses, draws (JSON file).
- Automated test suite for all game logic, AI and score management.
- Modular, well-documented source code for easy extension and educational use.

## Download & Play
- Download [tictactoe.exe](https://github.com/andres-montes-zuluaga/tictactoe/blob/main/dist/main.exe) from releases
- https://github.com/andres-montes-zuluaga/tictactoe/blob/main/dist/main.exe
- Double click to play!

## File Structure

tictactoe/<br>
│<br>
├── src/<br>
│ ├── gui.py # GUI layer and event logic (Pygame)<br>
│ ├── logic.py # Board class: game state and rules<br>
│ ├── ai.py # AI classes and decision logic<br>
│ ├── scores.py # Player stats: persistent scoreboard<br>
│<br>
├── data/<br>
│ └── scores.json # Player statistics (auto-managed)<br>
│<br>
├── tests/<br>
│ ├── test_logic.py # Board logic unit tests<br>
│ ├── test_ai.py # AI move selection tests<br>
│ ├── test_scores.py # Score persistence and leaderboard tests<br>
│ └── test_integration.py # Integration test for full game flow<br>
│<br>
├── main.py # Main entry point for launching the game<br>
├── README.md # Project documentation and instructions<br>


## Requirements

- Python 3.8+ (designed/tested with 3.11)
- Pygame (`pip install pygame`)
- [Optional] pytest or unittest for running tests

## Quick Start

1. **Clone the repository:**

git clone https://github.com/andres-montes-zuluaga/tictactoe.git
cd tictactoe

2. **Install dependencies and activate virtual environment:**

python -m venv venv
venv\Scripts\activate # Windows

or
source venv/bin/activate # Linux/Mac
pip install pygame

3. **Run the game:**

python main.py

## Running Tests

All logic and modules are covered by unittests.  
From your project root, run:

python -m unittest discover tests

text

Or run individual files (e.g.:)

python -m unittest tests/test_logic.py

## How It Works

- `main.py`: Boots the game, initializes Board, AI, GUI and launches the main loop.
- `src/logic.py`: Defines Board class, enforces game rules, tracks turns, checks winning/draw conditions.
- `src/ai.py`: Provides get_ai_player factory and implementations for three skill levels, including minimax.
- `src/scores.py`: Manages persistent player stats and leaderboard, stored in `data/scores.json`.
- `src/gui.py`: Draws all screens (menu, board, scoreboard), handles player input, integrates AI and rules.
- `tests/`: All modules have robust unit and integration tests.

## Screenshots

### Menu
<img width="594" height="628" alt="Menu" src="https://github.com/user-attachments/assets/d6e59d1a-eefc-4e69-aba0-f50c588d3926" />

### Board
<img width="594" height="622" alt="Board" src="https://github.com/user-attachments/assets/e24affce-186b-4b19-8f62-028466d6a87e" />

### Leaderboard
<img width="595" height="625" alt="Leaderboard" src="https://github.com/user-attachments/assets/2bc6c2b2-76e8-440e-a185-b93ac732bbd5" />


## Credits

Developed and maintained by Andrés Montes Zuluaga  
Licensed under the Apache License 2.0

---

For questions, issues or contributions, open a GitHub issue or contact the maintainer.
