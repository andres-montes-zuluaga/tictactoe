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
- Download the compressed file [tictactoe.rar](dist/TicTacToe.rar) (Right-click and choose "Save link as..." to download)
- Double click to play!

## File Structure

tictactoe/<br>
│<br>
├── src/<br>
│ ├── gui.py # GUI layer and event logic (Pygame)<br>
│ ├── logic.py # Board class: game state and rules<br>
│ ├── ai.py # AI classes and decision logic<br>
│ ├── scores.py # Persistent player stats and leaderboard<br>
│<br>
├── data/<br>
│ └── scores.json # Player statistics (auto-managed)<br>
│<br>
├── assets/<br>
│ └── bg.png # Background image<br>
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
<img width="598" height="629" alt="Menu" src="https://github.com/user-attachments/assets/61bbd154-c09a-488b-ab25-d2a3930614f8" />

### Board
<img width="597" height="628" alt="Board" src="https://github.com/user-attachments/assets/859126df-e459-4fe9-a611-8ba9ecbde793" />

### Leaderboard
<img width="599" height="629" alt="Leaderboard" src="https://github.com/user-attachments/assets/d34d0b55-348b-4cc7-ab52-045e76420550" />



## Credits

Developed and maintained by Andrés Montes Zuluaga  
Licensed under the Apache License 2.0

---

For questions, issues or contributions, open a GitHub issue or contact the maintainer.
