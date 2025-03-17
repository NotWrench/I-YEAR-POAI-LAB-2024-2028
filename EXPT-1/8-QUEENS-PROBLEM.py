from typing import List


class EightQueens:
    solution: List[List[int]] | None

    def __init__(self):
        self.solution = [[0 for _ in range(8)] for _ in range(8)]
        if not self.solve(0):
            self.solution = None

    def is_safe_to_move(self, row: int, col: int):
        for i in range(col):
            if self.solution[row][i] == 1:
                return False

        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if self.solution[i][j] == 1:
                return False

        for i, j in zip(range(row, 8, 1), range(col, -1, -1)):
            if self.solution[i][j] == 1:
                return False
        
        return True

    def solve(self, col: int):
        if col == 8:
            return True

        for i in range(8):
            if self.is_safe_to_move(i, col):
                self.solution[i][col] = 1
                if self.solve(col + 1):
                    return True
                self.solution[i][col] = 0

        return False

    def __str__(self):
        if self.solution is None:
            return "No solution found"

        return "\n".join(
            " ".join("Q" if cell == 1 else "-" for cell in row)
            for row in self.solution
        )
            

if __name__ == "__main__":
    eight_queens = EightQueens()
    print(eight_queens)
    