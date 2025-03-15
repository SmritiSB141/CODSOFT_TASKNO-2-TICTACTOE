import math
import tkinter as tk
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def get_columns(board):
    """Returns the columns of the board."""
    return [[board[0][i], board[1][i], board[2][i]] for i in range(3)]

def get_diagonal(board):
    """Returns the diagonals of the board."""
    return [[board[0][0], board[1][1], board[2][2]],
            [board[0][2], board[1][1], board[2][0]]]

def three_in_a_row(row):
    """Returns True if all elements in the row are the same and not None."""
    return row[0] == row[1] == row[2] != EMPTY

def player(board):
    """Returns the player who has the next turn (X or O)."""
    count_x = sum(row.count(X) for row in board)
    count_o = sum(row.count(O) for row in board)
    return O if count_x > count_o else X

def actions(board):
    """Returns a list of all possible actions (empty cells)."""
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY]

def result(board, action):
    """Returns the new board state after making a move."""
    i, j = action
    if board[i][j] != EMPTY:
        raise Exception("Invalid move")
    new_board = deepcopy(board)
    new_board[i][j] = player(board)
    return new_board

def winner(board):
    """Returns the winner of the game (X or O), or None if no winner yet."""
    rows = board + get_columns(board) + get_diagonal(board)
    for row in rows:
        if three_in_a_row(row):
            return row[0]
    return None

def terminal(board):
    """Returns True if the game is over (either win or draw)."""
    return winner(board) is not None or all(cell != EMPTY for row in board for cell in row)

def utility(board):
    """Returns 1 if X has won, -1 if O has won, 0 if it's a draw or game is ongoing."""
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

def minimax(board):
    """Returns the best score and the corresponding action for the current player."""
    if terminal(board):
        return utility(board), None

    if player(board) == X:
        return max_value(board)
    else:
        return min_value(board)

def max_value(board):
    """Returns the maximum value for X (maximize the score)."""
    max_eval = -math.inf
    best_action = None
    for action in actions(board):
        new_board = result(board, action)
        eval, _ = minimax(new_board)
        if eval > max_eval:
            max_eval = eval
            best_action = action
    return max_eval, best_action

def min_value(board):
    """Returns the minimum value for O (minimize the score)."""
    min_eval = math.inf
    best_action = None
    for action in actions(board):
        new_board = result(board, action)
        eval, _ = minimax(new_board)
        if eval < min_eval:
            min_eval = eval
            best_action = action
    return min_eval, best_action

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        
        # Initialize the game board
        self.board = initial_state()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        # Create a grid of buttons for the game board
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(root, text=" ", width=10, height=3,
                                                command=lambda row=i, col=j: self.player_move(row, col))
                self.buttons[i][j].grid(row=i, column=j)
        
        # Display the current player
        self.current_player_label = tk.Label(root, text="Current Player: X", font=("Arial", 14))
        self.current_player_label.grid(row=3, column=0, columnspan=3)

    def player_move(self, row, col):
        """Handles the player's move."""
        if self.board[row][col] == EMPTY:
            self.board[row][col] = X
            self.buttons[row][col].config(text=X)
            if terminal(self.board):
                self.end_game()
            else:
                self.current_player_label.config(text="Current Player: O")
                self.root.after(500, self.ai_move)  # Schedule AI move after player's move

    def ai_move(self):
        """AI makes its move using minimax."""
        print("AI is thinking...")
        _, (row, col) = minimax(self.board)
        self.board = result(self.board, (row, col))
        self.buttons[row][col].config(text=O)
        if terminal(self.board):
            self.end_game()
        else:
            self.current_player_label.config(text="Current Player: X")

    def end_game(self):
        """End the game when it's over."""
        winner_player = winner(self.board)
        if winner_player:
            self.current_player_label.config(text=f"Player {winner_player} wins!")
        else:
            self.current_player_label.config(text="It's a draw!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
