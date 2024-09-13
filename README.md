# Peg Solitaire Game

## Introduction
Peg Solitaire is a single-player puzzle game. The objective is to clear the board of all but one peg by jumping pegs over each other into empty holes.

## Game Modes
- **Easy Mode**: Full board with center hole empty.
- **Hard Mode**: Similar layout but with a different rule set (to be customized).

## How to Play
1. Start the game by selecting Easy or Hard mode.
2. Select a peg and choose an empty hole to move into.
3. Continue until only one peg remains or no valid moves are left.
4. You can undo or reset the game anytime.

## Installation Instructions
1. Install Flask:
pip install Flask

markdown
Copy code
2. Run the game:
python app.py

markdown
Copy code
The game will be available at `http://localhost:5000`.

## Features
- Easy and Hard game modes.
- Start, Stop, Pause buttons.
- Undo/Reset functionality.
- Board dynamically updates with each move.

## Technologies Used
- **Python (Flask)**: For the backend logic and game state management.
- **JavaScript**: For the frontend and user interaction.

## License
This project is licensed under the MIT License.
