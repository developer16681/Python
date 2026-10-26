"""
Experiment: Knapsack Problems (0/1 Dynamic Programming & Fractional Greedy)
----------------------------------------------------------------------------
Aim:
    To implement and contrast the two classic Knapsack problem formulations:
    1. 0/1 Knapsack: Solved via Dynamic Programming with item backtracking.
    2. Fractional Knapsack: Solved via the Greedy method by value-to-weight ratio.

Theory:
    Given a set of items, each with a weight and a value, determine the items to
    include in a collection so that the total weight does not exceed capacity W
    and total value is maximized.

    1. 0/1 Knapsack:
       Items cannot be broken into smaller pieces (take all or none).
       Recurrence:
       dp[i][w] = dp[i-1][w] if weights[i-1] > w else
                  max(dp[i-1][w], dp[i-1][w - weights[i-1]] + values[i-1])
       Time Complexity:  O(n * W)
       Space Complexity: O(n * W)

    2. Fractional Knapsack:
       Items can be subdivided. Greedy strategy sorts items by (value / weight) ratio.
       Time Complexity:  O(n log n)
       Space Complexity: O(1) auxiliary
"""

from typing import List, Tuple


def knapsack_01(weights: List[int], values: List[int], capacity: int) -> Tuple[int, List[int]]:
    """
    0/1 Knapsack using Dynamic Programming.
    Returns (max_value, selected_item_indices).
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # Build DP table
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

    # Backtrack to identify selected items
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i - 1)
            w -= weights[i - 1]

    selected_items.reverse()
    return dp[n][capacity], selected_items


def knapsack_fractional(weights: List[float], values: List[float], capacity: float) -> Tuple[float, List[Tuple[int, float]]]:
    """
    Fractional Knapsack using Greedy Algorithm.
    Returns (max_value, list of (item_index, fraction_taken)).
    """
    items = [(i, values[i], weights[i], values[i] / weights[i]) for i in range(len(weights))]
    # Sort descending by ratio (value / weight)
    items.sort(key=lambda x: x[3], reverse=True)

    total_value = 0.0
    current_capacity = capacity
    fractions_taken = []

    for idx, val, wt, ratio in items:
        if current_capacity <= 0:
            break

        if wt <= current_capacity:
            total_value += val
            current_capacity -= wt
            fractions_taken.append((idx, 1.0))
        else:
            fraction = current_capacity / wt
            total_value += val * fraction
            fractions_taken.append((idx, fraction))
            current_capacity = 0

    return total_value, fractions_taken


if __name__ == "__main__":
    print("=" * 65)
    print("     COLLEGE DSA LAB: 0/1 & FRACTIONAL KNAPSACK")
    print("=" * 65)

    wt = [10, 20, 30]
    val = [60, 100, 120]
    cap = 50

    print(f"Items: Weights = {wt}, Values = {val}, Knapsack Capacity = {cap}\n")

    # 1. 0/1 Knapsack
    max_val_01, items_01 = knapsack_01(wt, val, cap)
    print("--- 1. 0/1 Knapsack (Dynamic Programming) ---")
    print(f"Maximum Value Achieved: {max_val_01}")
    print(f"Selected Item Indices:  {items_01}")
    print(f"Selected Items Detail:  {[f'Item {i} (wt={wt[i]}, val={val[i]})' for i in items_01]}\n")

    # 2. Fractional Knapsack
    max_val_frac, items_frac = knapsack_fractional([float(x) for x in wt], [float(x) for x in val], float(cap))
    print("--- 2. Fractional Knapsack (Greedy Algorithm) ---")
    print(f"Maximum Value Achieved: {max_val_frac:.2f}")
    print("Fractions taken:")
    for idx, frac in items_frac:
        print(f"  Item {idx}: {frac * 100:.1f}% taken (Contributed: {val[idx] * frac:.1f})")
