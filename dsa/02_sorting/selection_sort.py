"""
Experiment: Selection Sort
---------------------------
Aim:
    To implement the Selection Sort algorithm in Python, demonstrate how the
    unsorted subarray's minimum element is iteratively placed at the beginning,
    and analyze its complexity.

Theory:
    Selection sort divides the input list into two parts: a sorted sublist of
    items built up from left to right, and a sublist of the remaining unsorted
    items. In each iteration, the minimum element from the unsorted sublist is
    selected and swapped with the leftmost unsorted element.

Time Complexity:
    - Best Case:    O(n^2)   (Requires n*(n-1)/2 comparisons regardless)
    - Average Case: O(n^2)
    - Worst Case:   O(n^2)

Space Complexity:
    - O(1) (In-place sorting algorithm)
Stability:
    - Unstable by default (e.g., swapping can alter relative order of duplicates)
"""

from typing import List


def selection_sort(arr: List[int]) -> List[int]:
    """
    Standard in-place Selection Sort.
    """
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def selection_sort_traced(arr: List[int]) -> List[int]:
    """
    Selection sort with step-by-step tracing of passes and swaps.
    """
    a = arr.copy()
    n = len(a)
    print(f"\nInitial Array: {a}")
    print("-" * 60)

    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j

        old_val = a[i]
        a[i], a[min_idx] = a[min_idx], a[i]
        print(f"Pass {i + 1:02d}: Min element {a[i]} (found at index {min_idx}) swapped with index {i} ({old_val})")
        print(f"         Sorted part: {a[:i + 1]} | Unsorted part: {a[i + 1:]}")

    print("-" * 60)
    print(f"Sorted Array: {a}\n")
    return a


if __name__ == "__main__":
    print("=" * 60)
    print("        COLLEGE DSA LAB: SELECTION SORT")
    print("=" * 60)

    data = [29, 10, 14, 37, 13]
    selection_sort_traced(data)
