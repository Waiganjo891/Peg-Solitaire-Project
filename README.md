# Peg Solitaire

This is a web-based implementation of the classic single-player puzzle game, **Peg Solitaire**. The game is built using Python's Flask framework for the backend API and JavaScript for rendering and controlling the game board on the frontend.

## Table of Contents

- [Project Overview](#project-overview)
- [Project Architecture](#project-architecture)
- [Setup Instructions](#setup-instructions)
- [Usage Guidelines](#usage-guidelines)
- [API Endpoints](#api-endpoints)

## Project Overview

Peg Solitaire is a game where the objective is to eliminate all but one peg by jumping one peg over another into an empty spot, removing the jumped peg. The game starts with a grid of pegs, and the player attempts to perform valid moves until only one peg remains.

### Features:
- Dynamic peg selection and movement
- Reset functionality to start a new game
- Undo functionality to reverse the last move
- Win or lose detection based on game state

## Project Architecture

### Backend (`app.py`)
- The backend is built using Flask, which provides a simple API to interact with the game board. It handles the game logic, validating moves, and tracking the state of the board.

### Frontend (`index.html`)
- The frontend is powered by HTML, CSS, and JavaScript. It renders the game board dynamically and interacts with the Flask backend to update the board after each move.

### Key Components:
- **`app.py`**: Implements the game logic and API endpoints.
- **`index.html`**: The main user interface, featuring buttons for resetting the game and undoing moves.
- **API Endpoints**: Used to fetch the current board, make moves, reset, and undo actions.

## Setup Instructions

To get the project up and running locally, follow these steps:

### Prerequisites
- Python 3.x
- Flask (`pip install Flask`)

### Steps:
1. Clone the repository to your local machine:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install Flask if you haven't already:
    ```bash
    pip install Flask
    ```

3. Run the Flask server:
    ```bash
    python3 app.py
    ```

4. Open your browser and navigate to `http://localhost:5000/` to start playing the game.

## Usage Guidelines

### Game Rules:
- Select a peg by clicking on it.
- Click on an empty cell to move the peg.
- Valid moves involve jumping over another peg horizontally or vertically.
- The game is won when only one peg remains.
- If no valid moves are left and more than one peg remains, the game is lost.

### Controls:
- **Reset**: Resets the board to its initial state.
- **Undo**: Reverts the last move made.

## API Endpoints

1. **`GET /board`**  
   Returns the current state of the game board.

   **Response:**
   ```json
   [
     [-1, -1, 1, 1, 1, -1, -1],
     [-1, 1, 1, 1, 1, 1, -1],
     [1, 1, 1, 0, 1, 1, 1],
     [1, 1, 1, 1, 1, 1, 1],
     [1, 1, 1, 1, 1, 1, 1],
     [-1, 1, 1, 1, 1, 1, -1],
     [-1, -1, 1, 1, 1, -1, -1],
   ]
