"""
Experiment: Jump Search and Ternary Search
-------------------------------------------
Aim:
    To implement Jump Search (Block Search) and Ternary Search algorithms
    on sorted arrays and evaluate their performance characteristics.

Theory:
    1. Jump Search:
       Works on sorted arrays. The optimal block size to jump is m = sqrt(n).
       Once a block is found where arr[prev] <= target <= arr[current],
       a linear search is performed within that block.
       Time Complexity: O(sqrt(n)), Space Complexity: O(1).

    2. Ternary Search:
       Similar to binary search, but divides the search space into three parts
       using two mid points:
       mid1 = low + (high - low) // 3
       mid2 = high - (high - low) // 3
       Time Complexity: O(log3 n), Space Complexity: O(1) or O(log3 n) recursive.
"""

import math
from typing import List


def jump_search(arr: List[int], target: int) -> int:
    """
    Performs Jump Search on a sorted array.
    
    Args:
        arr: Sorted list of integers.
        target: Value to find.
        
    Returns:
        Index of the target if found, else -1.
    """
    n = len(arr)
    if n == 0:
        return -1

    step = int(math.sqrt(n))
    prev = 0

    # Finding the block where the element is present (if it is present)
    while prev < n and arr[min(step, n) - 1] < target:
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            return -1

    # Linear search within the identified block
    while prev < min(step, n):
        if arr[prev] == target:
            return prev
        prev += 1

    return -1


def ternary_search_iterative(arr: List[int], target: int) -> int:
    """
    Iterative Ternary Search on a sorted array.
    """
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid1 = low + (high - low) // 3
        mid2 = high - (high - low) // 3

        if arr[mid1] == target:
            return mid1
        if arr[mid2] == target:
            return mid2

        if target < arr[mid1]:
            high = mid1 - 1
        elif target > arr[mid2]:
            low = mid2 + 1
        else:
            low = mid1 + 1
            high = mid2 - 1

    return -1


def ternary_search_recursive(arr: List[int], low: int, high: int, target: int) -> int:
    """
    Recursive Ternary Search on a sorted array.
    """
    if low > high:
        return -1

    mid1 = low + (high - low) // 3
    mid2 = high - (high - low) // 3

    if arr[mid1] == target:
        return mid1
    if arr[mid2] == target:
        return mid2

    if target < arr[mid1]:
        return ternary_search_recursive(arr, low, mid1 - 1, target)
    elif target > arr[mid2]:
        return ternary_search_recursive(arr, mid2 + 1, high, target)
    else:
        return ternary_search_recursive(arr, mid1 + 1, mid2 - 1, target)


if __name__ == "__main__":
    data = [1, 4, 7, 10, 14, 19, 22, 28, 33, 40, 48, 55, 63, 72, 85, 99]
    print("=" * 65)
    print("     COLLEGE DSA LAB: JUMP SEARCH & TERNARY SEARCH")
    print("=" * 65)
    print(f"Data array ({len(data)} elements): {data}\n")

    targets = [14, 85, 1, 99, 50]
    for t in targets:
        js = jump_search(data, t)
        ts_it = ternary_search_iterative(data, t)
        ts_rec = ternary_search_recursive(data, 0, len(data) - 1, t)
        print(f"Target: {t:>2} | Jump Search: {js:>2} | Ternary (Iter): {ts_it:>2} | Ternary (Rec): {ts_rec:>2}")
