from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def create_board():
    return [["" for _ in range(3)] for _ in range(3)]

def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != "":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        return board[0][2]
    return None if any("" in row for row in board) else "Draw"

def minimax(board, is_maximizing):
    winner = check_winner(board)
    if winner == "X":
        return -10
    elif winner == "O":
        return 10
    elif winner == "Draw":
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    score = minimax(board, False)
                    board[i][j] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    score = minimax(board, True)
                    board[i][j] = ""
                    best_score = min(score, best_score)
        return best_score

def best_move(board):
    best_score = -math.inf
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = "O"
                score = minimax(board, False)
                board[i][j] = ""
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

@app.route("/ai-move", methods=["POST"])
def ai_move():
    data = request.json
    board = data["board"]
    
    # Ensure the board is valid
    if not isinstance(board, list) or len(board) != 3 or any(len(row) != 3 for row in board):
        return jsonify({"error": "Invalid board format"}), 400
    
    ai_row, ai_col = best_move(board)
    
    # Check if a valid move is found
    if ai_row == -1 or ai_col == -1:
        return jsonify({"board": board, "winner": check_winner(board)})

    board[ai_row][ai_col] = "O"
    winner = check_winner(board)
    
    return jsonify({"board": board, "winner": winner})

if __name__ == "__main__":
    app.run(debug=True)
