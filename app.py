#!/usr/bin/python3
"""
Peg Solitaire Backend API using Flask.
This module provides a backend API for the Peg Solitaire game using Flask.
It defines several endpoints to interact with the game, including starting
a game, making moves, undoing moves, checking the game status, and resetting
the game. Module includes:
- `/board`: Returns the current board state.
- `/move`: Executes a move, validates it, and checks if the player won or lost.
- `/reset`: Resets the game board to the initial state.
- `/undo`: Undoes the last move.
"""
from flask import Flask, jsonify, request, render_template
from copy import deepcopy

app = Flask(__name__)

INITIAL_BOARD = [
    [-1, -1, 1, 1, 1, -1, -1],
    [-1,  1, 1, 1, 1,  1, -1],
    [1,  1, 1, 0, 1,  1,  1],
    [1,  1, 1, 1, 1,  1,  1],
    [1,  1, 1, 1, 1,  1,  1],
    [-1,  1, 1, 1, 1,  1, -1],
    [-1, -1, 1, 1, 1, -1, -1]
]

game_board = deepcopy(INITIAL_BOARD)
move_history = []


def is_valid_move(board, src, dst):
    """
    Check if a move from source (src) to destination (dst) is valid.
    A move is valid if:
    - The destination is empty (0).
    - The move is two steps horizontally or vertically.
    - A peg (1) is jumped over during the move.
    Args:
    board (list): The current game board.
    src (tuple): The source position as (x1, y1).
    dst (tuple): The destination position as (x2, y2).
    Returns:
    bool: True if the move is valid, False otherwise.
    """
    x1, y1 = src
    x2, y2 = dst

    if board[x2][y2] != 0:
        return False

    dx, dy = abs(x2 - x1), abs(y2 - y1)
    if (dx == 2 and dy == 0) or (dx == 0 and dy == 2):
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
        if board[mx][my] == 1 and board[x1][y1] == 1:
            return True
    return False


def apply_move(board, src, dst):
    """
    Apply a valid move on the board.
    Args:
    board (list): The current game board.
    src (tuple): The source position as (x1, y1).
    dst (tuple): The destination position as (x2, y2).
    Returns:
    None: The board is modified in-place.
    """
    x1, y1 = src
    x2, y2 = dst
    mx, my = (x1 + x2) // 2, (y1 + y2) // 2
    board[mx][my] = 0
    board[x2][y2] = 1
    board[x1][y1] = 0


def check_win(board):
    """
    Check if the game is won by having only one peg remaining.
    Args:
    board (list): The current game board.
    Returns:
    bool: True if only one peg remains, False otherwise.
    """
    return sum(row.count(1) for row in board) == 1


def has_valid_moves(board):
    """
    Check if there are any valid moves left on the board.
    Args:
    board (list): The current game board.
    Returns:
    bool: True if there are valid moves, False otherwise.
    """
    for i in range(7):
        for j in range(7):
            if board[i][j] == 1:
                for di, dj in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < 7 and 0 <= nj < 7 and is_valid_move(board, (i, j), (ni, nj)):
                        return True
    return False


@app.route('/')
def index():
    """
    Render the home page.
    Returns:
    str: The rendered HTML template for the homepage.
    """
    return render_template('index.html')


@app.route('/board', methods=['GET'])
def get_board():
    """
    API endpoint to get the current board state.
    Returns:
    json: JSON object representing the current game board.
    """
    return jsonify(game_board)


@app.route('/move', methods=['POST'])
def make_move():
    """
    API endpoint to make a move in the game.
    Accepts JSON data with `src` (source position)
    and `dst` (destination position) to perform a move.
    It checks the validity of the move and updates the board state.
    Returns:
    json: JSON object indicating the game status (`win`, `lose`,
    `continue`, `invalid`) and the current board state.
    """
    data = request.json
    src = tuple(data['src'])
    dst = tuple(data['dst'])

    if is_valid_move(game_board, src, dst):
        move_history.append(deepcopy(game_board))
        apply_move(game_board, src, dst)
        if check_win(game_board):
            return jsonify({"status": "win", "board": game_board})
        elif not has_valid_moves(game_board):
            return jsonify({"status": "lose", "board": game_board})
        return jsonify({"status": "continue", "board": game_board})
    return jsonify({"status": "invalid", "board": game_board})


@app.route('/reset', methods=['POST'])
def reset_game():
    """
    API endpoint to reset the game.
    Resets the game board to the initial configuration and clears
    the move history.
    Returns:
    json: JSON object representing the reset game board.
    """
    global game_board, move_history
    game_board = deepcopy(INITIAL_BOARD)
    move_history.clear()
    return jsonify(game_board)


@app.route('/undo', methods=['POST'])
def undo_move():
    """
    API endpoint to undo the last move.
    If there are previous moves in the history, it reverts
    the game board to the previous state.
    Returns:
    json: JSON object representing the updated game board.
    """
    if move_history:
        global game_board
        game_board = move_history.pop()
    return jsonify(game_board)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
