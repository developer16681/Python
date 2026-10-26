"""
Experiment: Bubble Sort and Optimized Bubble Sort
--------------------------------------------------
Aim:
    To implement the Bubble Sort algorithm in Python, optimize it with an early
    termination flag when no swaps occur, and analyze its pass-by-pass behavior.

Theory:
    Bubble Sort repeatedly steps through the list, compares adjacent elements,
    and swaps them if they are in the wrong order. The pass through the list
    is repeated until the list is sorted.
    With an optimization flag (swapped), if no swaps occur in a pass, the array
    is already sorted and execution can terminate early in O(n) time.

Time Complexity:
    - Best Case:    O(n)     (Already sorted array with optimization flag)
    - Average Case: O(n^2)
    - Worst Case:   O(n^2)   (Reverse sorted array)

Space Complexity:
    - O(1) (In-place sorting algorithm)
Stability:
    - Stable (Relative order of equal elements is preserved)
"""

from typing import List


def bubble_sort(arr: List[int]) -> List[int]:
    """
    Standard Bubble Sort with early exit optimization.
    Modifies array in-place and returns it.
    """
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def bubble_sort_traced(arr: List[int]) -> List[int]:
    """
    Bubble Sort with detailed step-by-step pass logging.
    """
    a = arr.copy()
    n = len(a)
    print(f"\nInitial Array: {a}")
    print("-" * 55)

    total_comparisons = 0
    total_swaps = 0

    for i in range(n - 1):
        swapped = False
        print(f"Pass {i + 1}:")
        for j in range(0, n - i - 1):
            total_comparisons += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
                total_swaps += 1
                print(f"  Swapped {a[j + 1]} and {a[j]} -> Current: {a}")
            else:
                print(f"  No swap for {a[j]} and {a[j + 1]}")

        if not swapped:
            print(f"--> Array sorted early at Pass {i + 1} (No swaps occurred).")
            break

    print("-" * 55)
    print(f"Sorting Complete: {a}")
    print(f"Total Comparisons: {total_comparisons}, Total Swaps: {total_swaps}\n")
    return a


if __name__ == "__main__":
    print("=" * 55)
    print("        COLLEGE DSA LAB: BUBBLE SORT")
    print("=" * 55)

    sample = [64, 34, 25, 12, 22, 11, 90]
    bubble_sort_traced(sample)

    already_sorted = [1, 2, 3, 4, 5]
    print("Testing Best-case (already sorted) with early exit:")
    bubble_sort_traced(already_sorted)
