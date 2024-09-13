#!/usr/bin/python3
"""
The server will handle initialization of the game board
and keep track of the state.
"""
from flask import Flask, jsonify, request

app = Flask(__name__)

EASY_BOARD = [
    [-1, -1, 1, 1, 1, -1, -1],
    [-1, 1, 1, 1, 1, 1, -1],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [-1, 1, 1, 1, 1, 1, -1],
    [-1, -1, 1, 1, 1, -1, -1],
]

HARD_BOARD = [
    [-1, -1, 1, 1, 1, -1, -1],
    [-1, 1, 1, 1, 1, 1, -1],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [-1, 1, 1, 1, 1, 1, -1],
    [-1, -1, 1, 1, 1, -1, -1],
]

game_state = {
    "board": [],
    "mode": "easy",
    "history": []
}


def reset_board(mode):
    """
    Resets the board game
    """
    if mode == "easy":
        game_state["board"] = [row[:] for row in EASY_BOARD]
    else:
        game_state["board"] = [row[:] for row in HARD_BOARD]
    game_state["history"] = []


def is_valid_move(board, from_pos, to_pos):
    """
    Checks if moves of user is valid or not
    If not: returns not
    if yes: returns new state as current state
    """
    x1, y1 = from_pos
    x2, y2 = to_pos
    if board[x1][y1] != 1 or board[x2][y2] != 0:
        return False
    if abs(x1 - x2) == 2 and y1 == y2:
        mid = (x1 + x2) // 2
        return board[mid][y1] == 1
    elif abs(y1 - y2) == 2 and x1 == x2:
        mid = (y1 + y2) // 2
        return board[x1][mid] == 1
    return False


def make_move(board, from_pos, to_pos):
    """
    Checks if move made is as per
    peg solitaire rules.
    """
    x1, y1 = from_pos
    x2, y2 = to_pos
    if abs(x1 - x2) == 2:
        mid = (x1 + x2) // 2
        board[x1][y1] = 0
        board[x2][y2] = 1
        board[mid][y1] = 0
    elif abs(y1 - y2) == 2:
        mid = (y1 + y2) // 2
        board[x1][y1] = 0
        board[x2][y2] = 1
        board[x1][mid] = 0


@app.route("/start", methods=["POST"])
def start_game():
    """
    API for start game.
    """
    mode = request.json.get("mode", "easy")
    game_state["mode"] = mode
    reset_board(mode)
    return jsonify({"board": game_state["board"]})


@app.route("/move", methods=["POST"])
def move():
    """
    API for move state in game
    """
    from_pos = request.json["from"]
    to_pos = request.json["to"]
    board = game_state["board"]
    if is_valid_move(board, from_pos, to_pos):
        game_state["history"].append([row[:] for row in board])
        make_move(board, from_pos, to_pos)
        return jsonify({"board": board, "status": "move_successful"})
    else:
        return jsonify({"error": "Invalid move"}), 400


@app.route("/undo", methods=["POST"])
def undo_move():
    """
    API route for undo a move
    """
    if game_state["history"]:
        game_state["board"] = game_state["history"].pop()
        return jsonify({"board": game_state["board"], "status": "undo_successful"})
    else:
        return jsonify({"error": "No moves to undo"}), 400


@app.route("/reset", methods=["POST"])
def reset_game():
    """
    API route for reset the game state as
    per game mode.
    """
    reset_board(game_state["mode"])
    return jsonify({"board": game_state["board"], "status": "reset_successful"})


@app.route("/state", methods=["GET"])
def get_state():
    """
    API route for get the game mode
    """
    return jsonify({"board": game_state["board"]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
