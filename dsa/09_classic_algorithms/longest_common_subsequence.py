"""
Experiment: Longest Common Subsequence (LCS) (Dynamic Programming)
-------------------------------------------------------------------
Aim:
    To implement the Longest Common Subsequence (LCS) algorithm using Dynamic
    Programming, compute the length of LCS, print the DP lookup table, and
    reconstruct the common subsequence string.

Theory:
    A subsequence is a sequence that can be derived from another sequence by
    deleting some or no elements without changing the order of the remaining elements.
    Given two sequences X[1..m] and Y[1..n], LCS finds the longest subsequence
    present in both.

Recurrence:
    - If X[i-1] == Y[j-1]: dp[i][j] = 1 + dp[i-1][j-1]
    - Else:                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

Time Complexity:
    - O(m * n) where m and n are string lengths.
Space Complexity:
    - O(m * n) for the DP table.
"""

from typing import List, Tuple


def lcs(x: str, y: str) -> Tuple[int, str, List[List[int]]]:
    """
    Computes Longest Common Subsequence.
    Returns (length, lcs_string, dp_table).
    """
    m, n = len(x), len(y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 1. Fill DP Table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # 2. Reconstruct LCS String from table
    lcs_chars = []
    i, j = m, n
    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            lcs_chars.append(x[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    lcs_chars.reverse()
    return dp[m][n], "".join(lcs_chars), dp


def print_dp_table(x: str, y: str, dp: List[List[int]]) -> None:
    print("\nDP Lookup Table:")
    header = "       " + "  ".join(f"'{ch}'" for ch in y)
    print(header)
    for i in range(len(dp)):
        row_label = f"'{x[i - 1]}'" if i > 0 else "'-'"
        row_str = "   ".join(f"{val:2d}" for val in dp[i])
        print(f"{row_label} | {row_str}")


if __name__ == "__main__":
    print("=" * 65)
    print("        COLLEGE DSA LAB: LONGEST COMMON SUBSEQUENCE")
    print("=" * 65)

    str1 = "LONGEST"
    str2 = "STONE"

    print(f"String 1 (X): '{str1}'")
    print(f"String 2 (Y): '{str2}'")

    length, lcs_str, table = lcs(str1, str2)

    print(f"\nLCS Length: {length}")
    print(f"LCS String: '{lcs_str}'")

    print_dp_table(str1, str2, table)

    # Classic University Example
    s1, s2 = "AGGTAB", "GXTXAYB"
    l, sub, _ = lcs(s1, s2)
    print(f"\nExample 2: '{s1}' and '{s2}' -> LCS: '{sub}' (Length: {l})")
