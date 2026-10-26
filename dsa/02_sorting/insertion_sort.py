"""
Experiment: Insertion Sort
---------------------------
Aim:
    To implement Insertion Sort in Python, demonstrate the shifting mechanism
    analogous to sorting playing cards in hand, and evaluate its performance.

Theory:
    Insertion sort works similarly to the way you sort playing cards in your
    hands. The array is virtually split into a sorted and an unsorted part.
    Values from the unsorted part are picked and placed at the correct position
    in the sorted part by shifting elements greater than the key to the right.

Time Complexity:
    - Best Case:    O(n)     (Array is already sorted; 1 comparison per element)
    - Average Case: O(n^2)
    - Worst Case:   O(n^2)   (Array is reverse sorted)

Space Complexity:
    - O(1) (In-place)
Stability:
    - Stable (Equal elements retain relative order)
"""

from typing import List


def insertion_sort(arr: List[int]) -> List[int]:
    """
    Standard in-place Insertion Sort.
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def insertion_sort_traced(arr: List[int]) -> List[int]:
    """
    Insertion Sort with step-by-step trace showing key selection and shifts.
    """
    a = arr.copy()
    n = len(a)
    print(f"\nInitial Array: {a}")
    print("-" * 65)

    for i in range(1, n):
        key = a[i]
        j = i - 1
        shifts = 0
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
            shifts += 1
        a[j + 1] = key

        print(f"Step {i:02d}: Inserted key={key:<3} at index {j + 1} (shifts={shifts}) -> {a}")

    print("-" * 65)
    print(f"Sorted Array: {a}\n")
    return a


if __name__ == "__main__":
    print("=" * 65)
    print("        COLLEGE DSA LAB: INSERTION SORT")
    print("=" * 65)

    data = [12, 11, 13, 5, 6]
    insertion_sort_traced(data)
