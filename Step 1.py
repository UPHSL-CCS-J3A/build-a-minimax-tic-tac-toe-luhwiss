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