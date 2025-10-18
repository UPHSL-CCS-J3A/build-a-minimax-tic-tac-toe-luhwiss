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
    
def minimax(board, player, me='O', opp='X'):
    """Return (best_value, best_move) assuming optimal play by both sides."""
    if terminal(board):
        return utility(board, me, opp), None

    # Initialize best value depending on whose turn it is
    best_val = -2 if player == me else 2
    best_move = None

    for m in moves(board):
        b2 = board[:]
        b2[m] = player
        # Switch turn: if player was me, next is opp; else me
        next_player = opp if player == me else me
        val, _ = minimax(b2, next_player, me, opp)

        if player == me and val > best_val:
            best_val, best_move = val, m
        elif player == opp and val < best_val:
            best_val, best_move = val, m

    return best_val, best_move

if __name__ == "__main__":
    # AI = 'O' to move, human = 'X'
    board = ['X','O','X',
             'O','X',' ',
             ' ','O',' ']
    print_board(board)
    val, move = minimax(board, player='O', me='O', opp='X')
    print("Minimax suggests move:", move, "with value:", val)

def play_game():
    board = [' '] * 9
    human = 'X'
    ai = 'O'

    print("Welcome to Tic-Tac-Toe (You are X, AI is O)")
    print_board(board)
    first = input("Do you want to go first? (y/n): ").strip().lower().startswith('y')
    current = human if first else ai

    while not terminal(board):
        if current == human:
            # Human move
            try:
                pos = int(input("Enter your move (1-9): ")) - 1
            except ValueError:
                print("Please enter a number 1-9.")
                continue
            if pos not in moves(board):
                print("Invalid move. Try again.")
                continue
            board[pos] = human
        else:
            # AI move
            print("AI is thinking...")
            _, m = minimax(board, player=ai, me=ai, opp=human)
            board[m] = ai
            print(f"AI chose position {m+1}")

        print_board(board)
        current = ai if current == human else human

    w = winner(board)
    if w == human:
        print("🎉 You win!")
    elif w == ai:
        print("🤖 AI wins!")
    else:
        print("😐 It's a draw!")

if __name__ == "__main__":
    play_game()

def alphabeta(board, player, alpha=-2, beta=2, me='O', opp='X'):
    if terminal(board):
        return utility(board, me, opp), None

 

    if player == me:
        best = (-2, None)  # MAX
        for m in moves(board):
            b2 = board[:]; b2[m] = player
            val, _ = alphabeta(b2, opp, alpha, beta, me, opp)
            if val > best[0]:
                best = (val, m)
            alpha = max(alpha, val)
            if alpha >= beta:  # prune
                break
        return best
    else:
        best = (2, None)   # MIN
        for m in moves(board):
            b2 = board[:]; b2[m] = player
            val, _ = alphabeta(b2, me, alpha, beta, me, opp)
            if val < best[0]:
                best = (val, m)
            beta = min(beta, val)
            if alpha >= beta:  # prune
                break
        return best
    
# Replace inside play_game (AI turn):
_, m = alphabeta(board, player=ai, alpha=-2, beta=2, me=ai, opp=human)