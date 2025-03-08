from typing import List


BOARD_SIZE = 8


def print_board(board: List[List[int]]) -> None:
    for row in board:
        row_str = ' '.join(str(col) for col in row)
        print(row_str)


def is_safe_to_move(board: List[List[int]], row: int, col: int) -> bool:
    for i in range(col):
        if board[row][i] == 1:
            return False
        
    upper_diagonal = zip(range(row, -1, -1), range(col, -1, -1))
    for i, j in upper_diagonal:
        if board[i][j] == 1:
            return False
        
    lower_digonal = zip(range(row, BOARD_SIZE), range(col, -1, -1))
    for i, j in lower_digonal:
        if board[i][j] == 1:
            return False
        
    return True


def place_queen(board: List[List[int]], col) -> bool:
    if col == BOARD_SIZE:
        print_board(board)
        return True
    
    for i in range(BOARD_SIZE):
        if is_safe_to_move(board, i, col):
            board[i][col] = 1
            if place_queen(board, i + 1):
                return True
            board[i][col] = 0

    return False


def solve_8_queens() -> bool:
    board = [[0 for i in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]

    if not place_queen(board, 0):
        print("No solution exists")
        return False

    return True


solve_8_queens()
