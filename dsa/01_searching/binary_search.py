"""
Experiment: Binary Search (Iterative, Recursive, and Bounds)
-------------------------------------------------------------
Aim:
    To implement Binary Search using both iterative and recursive approaches,
    find the first and last occurrences of elements in a sorted array, and
    analyze its logarithmic time complexity.

Theory:
    Binary Search is an efficient algorithm for finding an item from a sorted
    collection. It works by repeatedly dividing in half the portion of the list
    that could contain the item, until you've narrowed the possible locations
    to just one. The array MUST be sorted beforehand.

Time Complexity:
    - Best Case:    O(1)        (Target is the middle element)
    - Average Case: O(log n)
    - Worst Case:   O(log n)

Space Complexity:
    - Iterative: O(1)
    - Recursive: O(log n) due to call stack overhead.
"""

from typing import List, Tuple


def binary_search_iterative(arr: List[int], target: int) -> int:
    """
    Iterative implementation of Binary Search.
    
    Args:
        arr: Sorted list of integers.
        target: Value to find.
        
    Returns:
        Index of target in arr, or -1 if target is not found.
    """
    low = 0
    high = len(arr) - 1

    while low <= high:
        # Prevents integer overflow in languages with fixed int types
        mid = low + (high - low) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1


def binary_search_recursive(arr: List[int], low: int, high: int, target: int) -> int:
    """
    Recursive implementation of Binary Search.
    
    Args:
        arr: Sorted list of integers.
        low: Lower bound index of the current search window.
        high: Upper bound index of the current search window.
        target: Value to find.
        
    Returns:
        Index of target in arr, or -1 if target is not found.
    """
    if low > high:
        return -1

    mid = low + (high - low) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] > target:
        return binary_search_recursive(arr, low, mid - 1, target)
    else:
        return binary_search_recursive(arr, mid + 1, high, target)


def find_first_and_last_occurrence(arr: List[int], target: int) -> Tuple[int, int]:
    """
    Finds the first and last occurrence indices of target in a sorted list.
    """
    def find_bound(first: bool) -> int:
        low, high = 0, len(arr) - 1
        bound = -1
        while low <= high:
            mid = low + (high - low) // 2
            if arr[mid] == target:
                bound = mid
                if first:
                    high = mid - 1  # Continue searching left
                else:
                    low = mid + 1   # Continue searching right
            elif arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return bound

    return find_bound(first=True), find_bound(first=False)


def binary_search_visual_trace(arr: List[int], target: int) -> int:
    """
    Visualizes the search window and mid pointer at each step.
    """
    print(f"\nTracing Binary Search for target {target}:")
    print(f"Array: {arr}")
    print("-" * 65)
    print(f"{'Step':<6}{'Low':<6}{'Mid':<6}{'High':<6}{'arr[mid]':<10}{'Action'}")
    print("-" * 65)

    low = 0
    high = len(arr) - 1
    step = 1

    while low <= high:
        mid = low + (high - low) // 2
        mid_val = arr[mid]

        if mid_val == target:
            print(f"{step:<6}{low:<6}{mid:<6}{high:<6}{mid_val:<10}MATCH FOUND at index {mid}!")
            return mid
        elif mid_val < target:
            action = f"Target > {mid_val}: Move low to {mid + 1}"
            print(f"{step:<6}{low:<6}{mid:<6}{high:<6}{mid_val:<10}{action}")
            low = mid + 1
        else:
            action = f"Target < {mid_val}: Move high to {mid - 1}"
            print(f"{step:<6}{low:<6}{mid:<6}{high:<6}{mid_val:<10}{action}")
            high = mid - 1

        step += 1

    print(f"Target {target} not present in the array.")
    return -1


if __name__ == "__main__":
    sorted_array = [2, 5, 8, 12, 16, 23, 23, 23, 38, 56, 72, 91]
    target = 23

    print("=" * 65)
    print("        COLLEGE DSA LAB: BINARY SEARCH EXPERIMENT")
    print("=" * 65)

    # 1. Iterative
    res_iter = binary_search_iterative(sorted_array, target)
    print(f"Sorted Array: {sorted_array}")
    print(f"Iterative Binary Search for {target}: Index {res_iter}")

    # 2. Recursive
    res_rec = binary_search_recursive(sorted_array, 0, len(sorted_array) - 1, target)
    print(f"Recursive Binary Search for {target}: Index {res_rec}")

    # 3. First and Last Occurrences
    first, last = find_first_and_last_occurrence(sorted_array, target)
    print(f"Occurrences of {target}: First Index = {first}, Last Index = {last}")

    # 4. Search for element not in array
    missing = 45
    print(f"Search for {missing}: Index {binary_search_iterative(sorted_array, missing)}")

    # 5. Visual Step Trace
    binary_search_visual_trace(sorted_array, 56)
