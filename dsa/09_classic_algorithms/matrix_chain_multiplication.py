"""
Experiment: Matrix Chain Multiplication (Dynamic Programming)
--------------------------------------------------------------
Aim:
    To implement the Matrix Chain Multiplication algorithm in Python using
    Dynamic Programming to determine the optimal order of multiplying a chain
    of matrices, minimizing the number of scalar multiplications, and printing
    the parenthesized multiplication formula.

Theory:
    Given a sequence of matrices A_1, A_2, ..., A_n where matrix A_i has dimension
    p[i-1] x p[i], matrix multiplication is associative:
    (A * B) * C = A * (B * C), but the number of scalar multiplications differs
    dramatically depending on parenthesis placement.
    
    Recurrence:
    m[i, j] = 0 if i == j
    m[i, j] = min { m[i, k] + m[k+1, j] + p[i-1]*p[k]*p[j] } for i <= k < j

Time Complexity:
    - O(n^3) where n is number of matrices.
Space Complexity:
    - O(n^2) for cost table m and split bracket table s.
"""

from typing import List, Tuple


def matrix_chain_order(p: List[int]) -> Tuple[List[List[int]], List[List[int]]]:
    """
    Computes optimal matrix chain multiplication costs and bracket positions.
    p: List of dimensions where matrix A_i has dimension p[i-1] x p[i].
    """
    n = len(p) - 1  # Number of matrices
    # m[i][j] stores minimum cost of multiplying A_i..A_j
    m = [[0] * (n + 1) for _ in range(n + 1)]
    # s[i][j] stores the split point k
    s = [[0] * (n + 1) for _ in range(n + 1)]

    # chain_len is the length of the matrix chain
    for chain_len in range(2, n + 1):
        for i in range(1, n - chain_len + 2):
            j = i + chain_len - 1
            m[i][j] = float("inf")  # type: ignore

            for k in range(i, j):
                # cost = cost(A_i..A_k) + cost(A_{k+1}..A_j) + scalar product
                q = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k

    return m, s


def construct_parentheses(s: List[List[int]], i: int, j: int) -> str:
    """Recursively constructs parenthesized expression."""
    if i == j:
        return f"A{i}"
    else:
        k = s[i][j]
        left = construct_parentheses(s, i, k)
        right = construct_parentheses(s, k + 1, j)
        return f"({left} * {right})"


if __name__ == "__main__":
    print("=" * 65)
    print("     COLLEGE DSA LAB: MATRIX CHAIN MULTIPLICATION")
    print("=" * 65)

    # 4 Matrices:
    # A1: 10 x 30
    # A2: 30 x 5
    # A3: 5 x 60
    # Dimensions array: [10, 30, 5, 60]
    dims = [10, 30, 5, 60]
    num_mat = len(dims) - 1

    print(f"Matrix Chain Dimensions: {dims}")
    for idx in range(1, len(dims)):
        print(f"  Matrix A{idx}: {dims[idx-1]} x {dims[idx]}")

    cost_table, split_table = matrix_chain_order(dims)

    min_multiplications = cost_table[1][num_mat]
    optimal_formula = construct_parentheses(split_table, 1, num_mat)

    print(f"\nMinimum Scalar Multiplications Required: {min_multiplications}")
    print(f"Optimal Parenthesization Order:          {optimal_formula}")

    # Another standard university example: [40, 20, 30, 10, 30] (4 matrices)
    dims2 = [40, 20, 30, 10, 30]
    c2, s2 = matrix_chain_order(dims2)
    print(f"\nExample 2 Dimensions: {dims2}")
    print(f"Min Multiplications:  {c2[1][len(dims2)-1]}")
    print(f"Optimal Order:        {construct_parentheses(s2, 1, len(dims2)-1)}")
