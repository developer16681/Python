"""
Experiment: Merge Sort (Divide and Conquer)
--------------------------------------------
Aim:
    To implement the Merge Sort algorithm using the Divide-and-Conquer paradigm,
    trace sub-array divisions and merges, and count inversions.

Theory:
    Merge Sort is an efficient, comparison-based, divide-and-conquer algorithm.
    1. Divide: Divide the unsorted list into two approximately equal halves.
    2. Conquer: Recursively sort the two halves.
    3. Combine: Merge the two sorted halves into a single sorted list.

Recurrence Relation:
    T(n) = 2 * T(n / 2) + Theta(n)
    Solving via Master Theorem yields Theta(n log n).

Time Complexity:
    - Best Case:    O(n log n)
    - Average Case: O(n log n)
    - Worst Case:   O(n log n)

Space Complexity:
    - O(n) (Requires auxiliary array space for merging)
Stability:
    - Stable
"""

from typing import List, Tuple


def merge(left: List[int], right: List[int]) -> List[int]:
    """
    Merges two sorted lists into a single sorted list.
    """
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # <= ensures stability
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Append remaining elements
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def merge_sort(arr: List[int]) -> List[int]:
    """
    Recursive Merge Sort returning a new sorted list.
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge_sort_traced(arr: List[int], depth: int = 0) -> List[int]:
    """
    Recursive Merge Sort with hierarchical visual indentation.
    """
    indent = "  " * depth
    if len(arr) <= 1:
        print(f"{indent}Base case reached: {arr}")
        return arr

    mid = len(arr) // 2
    print(f"{indent}Dividing {arr} -> Left: {arr[:mid]}, Right: {arr[mid:]}")

    left = merge_sort_traced(arr[:mid], depth + 1)
    right = merge_sort_traced(arr[mid:], depth + 1)

    merged = merge(left, right)
    print(f"{indent}Merged {left} and {right} -> {merged}")
    return merged


def count_inversions_and_sort(arr: List[int]) -> Tuple[List[int], int]:
    """
    Counts total inversions in array using modified Merge Sort in O(n log n).
    An inversion is a pair (i, j) such that i < j and arr[i] > arr[j].
    """
    if len(arr) <= 1:
        return arr, 0

    mid = len(arr) // 2
    left, inv_left = count_inversions_and_sort(arr[:mid])
    right, inv_right = count_inversions_and_sort(arr[mid:])

    merged = []
    i = j = 0
    inversions = inv_left + inv_right

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            inversions += len(left) - i  # all remaining elements in left are inversions
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, inversions


if __name__ == "__main__":
    print("=" * 60)
    print("        COLLEGE DSA LAB: MERGE SORT")
    print("=" * 60)

    sample = [38, 27, 43, 3, 9, 82, 10]
    print(f"Original Array: {sample}\n")

    print("Step-by-step Divide and Conquer trace:")
    sorted_res = merge_sort_traced(sample)
    print(f"\nFinal Sorted Array: {sorted_res}")

    # Counting inversions
    inv_data = [8, 4, 2, 1]
    _, inv_count = count_inversions_and_sort(inv_data)
    print(f"\nInversions in {inv_data}: {inv_count} (Expected 6 for reverse order)")
