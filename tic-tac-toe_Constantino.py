def print_board(board):
    """Display board in a 3x3 grid."""
    print("\n")
    for i in range(0, 9, 3):
        a, b, c = board[i], board[i+1], board[i+2]
        print(f" {a} | {b} | {c} ")
        if i < 6:
            print("---+---+---")
    print("\n")

if __name__ == "__main__":  # quick test
    board = [' '] * 9
    print_board(board)

# --- GAME RULES ---

# All winning triplets (rows, columns, diagonals)
LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]

def winner(board):
    """Return 'X' or 'O' if someone has three in a row, else None."""
    for a, b, c in LINES:
        if board[a] != ' ' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def moves(board):
    """List of indices that are empty."""
    return [i for i, v in enumerate(board) if v == ' ']

def terminal(board):
    """True if the game is over (win or draw)."""
    return winner(board) is not None or not moves(board)

if __name__ == "__main__":
    b = ['X','X','X',' ',' ',' ',' ',' ',' ']
    print_board(b)
    print("Winner should be X ->", winner(b))
    print("Moves available ->", moves(b))
    print("Terminal? ->", terminal(b))

def utility(board, me='O', opp='X'):
    """Score terminal states from AI perspective: +1 win, -1 loss, 0 draw."""
    w = winner(board)
    if w == me:
        return 1
    elif w == opp:
        return -1
    else:
        return 0  # draw or non-terminal (we only call this at terminal)