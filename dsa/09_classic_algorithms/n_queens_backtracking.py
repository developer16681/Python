"""
Experiment: N-Queens Problem (Backtracking)
--------------------------------------------
Aim:
    To implement the N-Queens problem using Backtracking in Python, finding
    all distinct solutions where N non-attacking queens are placed on an N x N
    chessboard, and visualising board configurations.

Theory:
    The N-Queens puzzle is the problem of placing N chess queens on an N x N
    chessboard so that no two queens threaten each other. Thus, a solution requires
    that no two queens share the same row, column, or diagonal.
    
    Backtracking Strategy:
    - Place queens column by column.
    - If all queens are placed successfully, save solution.
    - Try all rows in the current column. If safe, mark cell and recursively
      try placing queens in remaining columns.
    - If placing queen does not lead to a valid configuration, backtrack (remove queen).

Time Complexity:
    - O(N!) in worst-case exploration.
Space Complexity:
    - O(N) for recursion stack and position arrays.
"""

from typing import List


def solve_n_queens(n: int) -> List[List[str]]:
    """
    Finds all valid N-Queens configurations.
    Returns list of boards, each represented as a list of string rows.
    """
    solutions: List[List[str]] = []
    # cols[c] is True if column c has a queen
    cols = [False] * n
    # diag1[r - c + n - 1] is True if main diagonal (\) has a queen
    diag1 = [False] * (2 * n - 1)
    # diag2[r + c] is True if anti-diagonal (/) has a queen
    diag2 = [False] * (2 * n - 1)

    # board[r] stores the column index of queen in row r
    queens_in_rows = [-1] * n

    def backtrack(row: int):
        if row == n:
            # Build string board representation
            board = []
            for r in range(n):
                c = queens_in_rows[r]
                row_str = ". " * c + "Q " + ". " * (n - c - 1)
                board.append(row_str.strip())
            solutions.append(board)
            return

        for col in range(n):
            d1_idx = row - col + n - 1
            d2_idx = row + col

            if not cols[col] and not diag1[d1_idx] and not diag2[d2_idx]:
                # Place queen
                queens_in_rows[row] = col
                cols[col] = diag1[d1_idx] = diag2[d2_idx] = True

                backtrack(row + 1)

                # Backtrack / remove queen
                cols[col] = diag1[d1_idx] = diag2[d2_idx] = False
                queens_in_rows[row] = -1

    backtrack(0)
    return solutions


def print_board(board: List[str], sol_num: int) -> None:
    print(f"\nSolution #{sol_num}:")
    n = len(board)
    print("+" + "---" * n + "+")
    for row in board:
        print(f"| {row} |")
    print("+" + "---" * n + "+")


if __name__ == "__main__":
    print("=" * 65)
    print("        COLLEGE DSA LAB: N-QUEENS BACKTRACKING")
    print("=" * 65)

    n = 4
    solutions = solve_n_queens(n)

    print(f"Found {len(solutions)} distinct solutions for N = {n} Queens:\n")
    for idx, sol in enumerate(solutions, 1):
        print_board(sol, idx)

    # Quick check for N = 8 standard chessboard count
    n8_solutions = solve_n_queens(8)
    print(f"\nTotal solutions for standard 8-Queens problem: {len(n8_solutions)} (Expected: 92)")
