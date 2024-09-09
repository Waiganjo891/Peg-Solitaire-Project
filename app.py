#!/usr/bin/python3
"""
The server will handle initialization of the game board
and keep track of the state.
"""
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


def initialize_board():
    """
    Initialize the board with a typical Peg Solitaire layout (7x7 grid)
    """
    board = [
        [-1, -1, 1, 1, 1, -1, -1],
        [-1, -1, 1, 1, 1, -1, -1],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [-1, -1, 1, 1, 1, -1, -1],
        [-1, -1, 1, 1, 1, -1, -1]
    ]
    return board


def is_valid_move(board, x1, y1, x2, y2):
    """
    Check if a move is valid
    """
    if board[x1][y1] == 1 and board[x2][y2] == 0:
        if (x1 == x2 and abs(y1 - y2) == 2) or (y1 == y2 and abs(x1 - x2) == 2):
            middle_x, middle_y = (x1 + x2) // 2, (y1 + y2) // 2
            if board[middle_x][middle_y] == 1:
                return True
    return False


def execute_move(board, x1, y1, x2, y2):
    """
    Execute the move and remove the jumped peg
    """
    middle_x, middle_y = (x1 + x2) // 2, (y1 + y2) // 2
    board[x1][y1] = 0
    board[middle_x][middle_y] = 0
    board[x2][y2] = 1
    return board


def check_game_over(board):
    """
    Check if the player won or lost
    """
    valid_moves_exist = False
    peg_count = 0

    for x in range(7):
        for y in range(7):
            if board[x][y] == 1:
                peg_count += 1
                if x > 1 and is_valid_move(board, x, y, x-2, y):
                    valid_moves_exist = True
                if x < 5 and is_valid_move(board, x, y, x+2, y):
                    valid_moves_exist = True
                if y > 1 and is_valid_move(board, x, y, x, y-2):
                    valid_moves_exist = True
                if y < 5 and is_valid_move(board, x, y, x, y+2):
                    valid_moves_exist = True
    if peg_count == 1:
        return "win"
    elif not valid_moves_exist:
        return "lose"
    return "continue"


@app.route('/')
def index():
    """
    Run index.html
    """
    return render_template('index.html')


@app.route('/new_game', methods=['GET'])
def new_game():
    """
    Start a new game
    """
    board = initialize_board()
    return jsonify(board=board, game_status="continue")


@app.route('/move', methods=['POST'])
def make_move():
    """
    Logic for moving pegs
    """
    data = request.json
    board = data['board']
    x1, y1 = data['start']
    x2, y2 = data['end']
    if is_valid_move(board, x1, y1, x2, y2):
        board = execute_move(board, x1, y1, x2, y2)
        game_status = check_game_over(board)
        return jsonify(board=board, game_status=game_status)
    else:
        return jsonify(error="Invalid move"), 400


@app.route('/reset', methods=['POST'])
def reset_game():
    """
    Reset the game
    """
    board = initialize_board()
    return jsonify(board=board, game_status="continue")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
