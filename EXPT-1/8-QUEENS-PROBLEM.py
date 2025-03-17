from typing import List


class EightQueens:
    n: int = 8
    board: List[List[int]]
    solution: List[List[int]]

    def __init__(self):
        self.n = n
        self.board = [[0 for _ in range(n)] for _ in range(n)]
        self.solution = [[0 for _ in range(n)] for _ in range(n)]

    def is_safe_to_move(self, row: int, col: int):
        for i in range(col):
            if self.solution[row][i] == 1:
                return False

        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if self.solution[i][j] == 1:
                return False

        for i, j in zip(range(row, self.n, 1), range(col, -1, -1)):
            if self.solution[i][j] == 1:
                return False
        
        return True

    def solve(self, col: int):
        if col == self.n:
            return True

        for i in range(self.n):
            if self.is_safe_to_move(i, col):
                self.solution[i][col] = 1
                if self.solve(col + 1):
                    return True
                self.solution[i][col] = 0

        return False

    def __str__(self):
        if not self.solve(0):
            return "No solution found"

        return "\n".join(
            " ".join("Q" if cell == 1 else "-" for cell in row)
            for row in self.solution
        )
            

if __name__ == "__main__":
    eight_queens = EightQueens()
    eight_queens.solve(0)
    print(eight_queens)
    