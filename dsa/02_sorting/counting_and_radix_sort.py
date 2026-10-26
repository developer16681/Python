"""
Experiment: Counting Sort and Radix Sort (Non-Comparison Sorting)
-----------------------------------------------------------------
Aim:
    To implement Counting Sort and Radix Sort algorithms in Python, demonstrate
    how non-comparison sorting achieves linear time O(n) under specific conditions,
    and evaluate digit-by-digit sorting with Radix Sort.

Theory:
    1. Counting Sort:
       Operating on keys between a specific range [0, k], Counting Sort counts
       occurrences of each value, computes prefix sums for target positions,
       and constructs the sorted array in stable order.
       Time: O(n + k), Space: O(n + k).

    2. Radix Sort:
       Sorts integers digit-by-digit from least significant digit (LSD) to most
       significant digit (MSD) using Counting Sort as a stable sub-routine.
       Time: O(d * (n + b)) where d is max digits, b is base (10).
       Space: O(n + b).
"""

from typing import List


def counting_sort(arr: List[int]) -> List[int]:
    """
    Stable Counting Sort for non-negative integers.
    """
    if not arr:
        return []

    max_val = max(arr)
    count = [0] * (max_val + 1)
    output = [0] * len(arr)

    # Store count of each element
    for num in arr:
        count[num] += 1

    # Cumulative count (prefix sum) gives the actual positions
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    # Build the output array in reverse order to ensure stability
    for num in reversed(arr):
        output[count[num] - 1] = num
        count[num] -= 1

    return output


def _counting_sort_by_digit(arr: List[int], exp: int) -> None:
    """
    Helper stable counting sort for a specific digit place (exp = 1, 10, 100, ...).
    """
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    # Store count of occurrences of digit (arr[i] // exp) % 10
    for i in range(n):
        digit = (arr[i] // exp) % 10
        count[digit] += 1

    # Cumulative count
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build output array (reverse for stability)
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1

    # Copy output to original array
    for i in range(n):
        arr[i] = output[i]


def radix_sort(arr: List[int]) -> List[int]:
    """
    LSD Radix Sort for non-negative integers.
    """
    if not arr:
        return []

    a = arr.copy()
    max_val = max(a)

    exp = 1
    pass_num = 1
    print(f"\nInitial Array for Radix Sort: {a}")
    print("-" * 55)

    while max_val // exp > 0:
        _counting_sort_by_digit(a, exp)
        print(f"Pass {pass_num} (Sorting by {exp:>4}'s place): {a}")
        exp *= 10
        pass_num += 1

    print("-" * 55)
    return a


if __name__ == "__main__":
    print("=" * 55)
    print("     COLLEGE DSA LAB: COUNTING SORT & RADIX SORT")
    print("=" * 55)

    # 1. Counting Sort
    raw_data = [4, 2, 2, 8, 3, 3, 1]
    sorted_counting = counting_sort(raw_data)
    print(f"Original for Counting Sort: {raw_data}")
    print(f"Counting Sort Output:       {sorted_counting}\n")

    # 2. Radix Sort
    large_numbers = [170, 45, 75, 90, 802, 24, 2, 66]
    sorted_radix = radix_sort(large_numbers)
    print(f"Radix Sort Final Output:    {sorted_radix}")
