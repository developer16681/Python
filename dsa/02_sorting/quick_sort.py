"""
Experiment: Quick Sort (Partitioning Strategies)
-------------------------------------------------
Aim:
    To implement Quick Sort using both Lomuto and Hoare partitioning schemes,
    demonstrate pivot selection, and analyze worst-case vs average-case behavior.

Theory:
    Quick Sort is a Divide-and-Conquer algorithm. It picks an element as pivot
    and partitions the given array around the picked pivot such that:
    - All elements smaller than the pivot come before it.
    - All elements greater than the pivot come after it.
    The sub-arrays are then recursively sorted.

Partition Schemes:
    1. Lomuto Partition: Pivot is typically the last element. Simple to implement.
    2. Hoare Partition: Pivot is first element. Uses two pointers moving towards
       each other. Requires about 3x fewer swaps on average than Lomuto.

Time Complexity:
    - Best Case:    O(n log n)  (Balanced partitions)
    - Average Case: O(n log n)
    - Worst Case:   O(n^2)      (Already sorted array with extreme pivot choice)

Space Complexity:
    - O(log n) auxiliary stack space in average case, O(n) in worst case.
Stability:
    - Unstable
"""

from typing import List


def lomuto_partition(arr: List[int], low: int, high: int) -> int:
    """
    Lomuto partition scheme: pivot is arr[high].
    """
    pivot = arr[high]
    i = low - 1  # Index of smaller element

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort_lomuto(arr: List[int], low: int, high: int) -> None:
    """
    Quick sort using Lomuto partition. Sorts in-place.
    """
    if low < high:
        pi = lomuto_partition(arr, low, high)
        quick_sort_lomuto(arr, low, pi - 1)
        quick_sort_lomuto(arr, pi + 1, high)


def hoare_partition(arr: List[int], low: int, high: int) -> int:
    """
    Hoare partition scheme: pivot is arr[low].
    Two pointers traverse inwards until an inversion is found.
    """
    pivot = arr[low]
    i = low - 1
    j = high + 1

    while True:
        i += 1
        while arr[i] < pivot:
            i += 1

        j -= 1
        while arr[j] > pivot:
            j -= 1

        if i >= j:
            return j

        arr[i], arr[j] = arr[j], arr[i]


def quick_sort_hoare(arr: List[int], low: int, high: int) -> None:
    """
    Quick sort using Hoare partition. Sorts in-place.
    """
    if low < high:
        pi = hoare_partition(arr, low, high)
        quick_sort_hoare(arr, low, pi)
        quick_sort_hoare(arr, pi + 1, high)


def quick_sort_traced(arr: List[int], low: int, high: int, depth: int = 0) -> None:
    """
    Quick Sort with visual call-stack trace showing pivot choices.
    """
    indent = "  " * depth
    if low < high:
        pivot = arr[high]
        print(f"{indent}Sub-array {arr[low:high + 1]} | Pivot = {pivot}")
        pi = lomuto_partition(arr, low, high)
        print(f"{indent}After partition: {arr[low:high + 1]} (Pivot at index {pi})")

        quick_sort_traced(arr, low, pi - 1, depth + 1)
        quick_sort_traced(arr, pi + 1, high, depth + 1)


if __name__ == "__main__":
    print("=" * 60)
    print("        COLLEGE DSA LAB: QUICK SORT")
    print("=" * 60)

    # 1. Lomuto Partition Test
    arr1 = [10, 80, 30, 90, 40, 50, 70]
    print(f"Original Array: {arr1}")
    print("\nTracing Quick Sort (Lomuto Scheme):")
    quick_sort_traced(arr1, 0, len(arr1) - 1)
    print(f"Sorted Result (Lomuto): {arr1}\n")

    # 2. Hoare Partition Test
    arr2 = [10, 80, 30, 90, 40, 50, 70]
    quick_sort_hoare(arr2, 0, len(arr2) - 1)
    print(f"Sorted Result (Hoare Scheme): {arr2}")
