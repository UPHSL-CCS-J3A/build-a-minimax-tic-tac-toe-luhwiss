import tkinter as tk
from tkinter import messagebox

def print_board(board):
    """Display board in a 3x3 grid."""
    print("\n")
    for i in range(0, 9, 3):
        a, b, c = board[i], board[i+1], board[i+2]
        print(f" {a} | {b} | {c} ")
        if i < 6:
            print("---+---+---")
    print("\n")

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
            # Replace inside play_game (AI turn):
            _, m = alphabeta(board, player=ai, alpha=-2, beta=2, me=ai, opp=human)
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

class TicTacToeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")
        self.root.geometry("300x250")
        self.root.resizable(False, False)
        self.board = [' '] * 9
        self.human = 'X'
        self.ai = 'O'
        self.current = self.human
        self.buttons = []
        self.show_instructions()
        
    def show_instructions(self):
        tk.Label(self.root, text="Tic-Tac-Toe", font=('Arial', 18, 'bold')).pack(pady=10)
        tk.Label(self.root, text="Instructions:", font=('Arial', 12, 'bold')).pack()
        tk.Label(self.root, text="• You are X, AI is O").pack()
        tk.Label(self.root, text="• Click any cell to make your move").pack()
        tk.Label(self.root, text="• Get 3 in a row to win!").pack(pady=(0,10))
        tk.Label(self.root, text="Who goes first?", font=('Arial', 11, 'bold')).pack()
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="I go first", font=('Arial', 10), 
                 command=lambda: self.start_game(True)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="AI goes first", font=('Arial', 10), 
                 command=lambda: self.start_game(False)).pack(side='left', padx=5)
    
    def start_game(self, human_first=True):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.geometry("240x280")
        self.human_first = human_first
        self.create_widgets()
        if not human_first:
            self.ai_move()
        
    def create_widgets(self):
        for i in range(9):
            btn = tk.Button(self.root, text=' ', font=('Arial', 24, 'bold'), width=3, height=1,
                          command=lambda i=i: self.make_move(i))
            btn.grid(row=i//3, column=i%3, padx=1, pady=1, sticky='nsew')
            self.buttons.append(btn)
        
        for i in range(3):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)
        
        restart_btn = tk.Button(self.root, text="New Game", font=('Arial', 10),
                              command=self.restart_game)
        restart_btn.grid(row=3, column=0, columnspan=3, pady=5, sticky='ew')
        
    def make_move(self, pos):
        if self.board[pos] != ' ' or terminal(self.board):
            return
            
        self.board[pos] = self.human
        self.buttons[pos].config(text=self.human, state='disabled')
        
        if terminal(self.board):
            self.end_game()
            return
            
        self.ai_move()
    
    def ai_move(self):
        if terminal(self.board):
            return
        _, ai_pos = alphabeta(self.board, self.ai, me=self.ai, opp=self.human)
        if ai_pos is not None:
            self.board[ai_pos] = self.ai
            self.buttons[ai_pos].config(text=self.ai, state='disabled')
            
        if terminal(self.board):
            self.end_game()
            
    def end_game(self):
        w = winner(self.board)
        if w == self.human:
            messagebox.showinfo("Game Over", "🎉 You win!")
        elif w == self.ai:
            messagebox.showinfo("Game Over", "🤖 AI wins!")
        else:
            messagebox.showinfo("Game Over", "😐 It's a draw!")
            
    def restart_game(self):
        self.board = [' '] * 9
        for btn in self.buttons:
            btn.config(text=' ', state='normal')
        if not self.human_first:
            self.ai_move()
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = TicTacToeGUI()
    game.run() 

