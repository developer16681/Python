"""
Experiment: Linear Search and Variations
-----------------------------------------
Aim:
    To implement Linear Search, Sentinel Linear Search, and Multi-occurrence
    Search algorithms in Python and analyze their time and space complexities.

Theory:
    Linear search is the simplest searching algorithm that checks every element
    in a list sequentially until the target element is found or the end of the
    list is reached. It works on both sorted and unsorted lists.

Time Complexity:
    - Best Case:    O(1)     (Element found at the first position)
    - Average Case: O(n)
    - Worst Case:   O(n)     (Element at the last position or absent)

Space Complexity:
    - O(1) (In-place search, requires no auxiliary memory)
"""

from typing import Any, List, Optional, Tuple


def linear_search(arr: List[Any], target: Any) -> int:
    """
    Standard Linear Search.
    
    Args:
        arr: List of elements to search through.
        target: Value to find.
        
    Returns:
        Index of the first occurrence of target, or -1 if not found.
    """
    for index, value in enumerate(arr):
        if value == target:
            return index
    return -1


def sentinel_linear_search(arr: List[Any], target: Any) -> int:
    """
    Sentinel Linear Search.
    Reduces the number of comparisons per iteration by placing the target
    at the end of the array as a sentinel, eliminating the boundary check.
    
    Args:
        arr: List of elements.
        target: Value to find.
        
    Returns:
        Index of the target if found within original bounds, else -1.
    """
    n = len(arr)
    if n == 0:
        return -1

    last = arr[-1]
    arr[-1] = target
    i = 0
    while arr[i] != target:
        i += 1

    # Restore the original last element
    arr[-1] = last

    if i < n - 1 or arr[-1] == target:
        return i
    return -1


def linear_search_all_occurrences(arr: List[Any], target: Any) -> List[int]:
    """
    Finds all indices where the target occurs in the array.
    """
    return [i for i, val in enumerate(arr) if val == target]


def linear_search_visual_trace(arr: List[int], target: int) -> int:
    """
    Demonstrates linear search step-by-step with console visualization.
    """
    print(f"\nSearching for {target} in array: {arr}")
    print("-" * 50)
    for i, val in enumerate(arr):
        match = "MATCH FOUND!" if val == target else "No match"
        print(f"Step {i + 1:02d}: Checking index [{i}] -> Value: {val} | {match}")
        if val == target:
            print(f"--> Target {target} found at index {i}.")
            return i
    print(f"--> Target {target} not found in array.")
    return -1


if __name__ == "__main__":
    sample_data = [42, 17, 89, 23, 56, 12, 78, 23, 90]
    target_val = 23

    print("=" * 60)
    print("        COLLEGE DSA LAB: LINEAR SEARCH EXPERIMENT")
    print("=" * 60)

    # 1. Standard Linear Search
    idx = linear_search(sample_data, target_val)
    print(f"Data: {sample_data}")
    print(f"Standard Linear Search: Target {target_val} found at index {idx}")

    # 2. All occurrences
    indices = linear_search_all_occurrences(sample_data, target_val)
    print(f"All Occurrences of {target_val}: indices {indices}")

    # 3. Sentinel Linear Search
    sentinel_idx = sentinel_linear_search(sample_data.copy(), target_val)
    print(f"Sentinel Search: Target {target_val} found at index {sentinel_idx}")

    # 4. Search for absent element
    absent = 999
    print(f"Search for absent element ({absent}): {linear_search(sample_data, absent)}")

    # 5. Visual Step-by-Step Trace
    linear_search_visual_trace([15, 32, 8, 44, 21], 44)
