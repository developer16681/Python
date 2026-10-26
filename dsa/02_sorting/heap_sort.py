"""
Experiment: Heap Sort
----------------------
Aim:
    To implement the Heap Sort algorithm using a Binary Max-Heap, understand
    the heapify procedure, and verify its O(n log n) guaranteed time complexity.

Theory:
    Heap Sort is a comparison-based sorting technique based on Binary Heap data
    structure. It is similar to selection sort where we first find the maximum
    element and place the maximum element at the end. We repeat the same process
    for remaining elements.
    
    Steps:
    1. Build a max heap from the input data.
    2. At this point, the largest item is stored at the root of the heap.
       Replace it with the last item of the heap followed by reducing the
       size of heap by 1.
    3. Heapify the root of the tree.
    4. Repeat step 2 while size of heap is greater than 1.

Time Complexity:
    - Best Case:    O(n log n)
    - Average Case: O(n log n)
    - Worst Case:   O(n log n)  (Guaranteed, unlike Quick Sort)

Space Complexity:
    - O(1) (In-place)
Stability:
    - Unstable
"""

from typing import List


def heapify(arr: List[int], n: int, i: int) -> None:
    """
    To heapify a subtree rooted with node i which is an index in arr[].
    n is size of heap.
    """
    largest = i          # Initialize largest as root
    left = 2 * i + 1     # left child index
    right = 2 * i + 2    # right child index

    # If left child is larger than root
    if left < n and arr[left] > arr[largest]:
        largest = left

    # If right child is larger than largest so far
    if right < n and arr[right] > arr[largest]:
        largest = right

    # If largest is not root
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # swap
        # Recursively heapify the affected sub-tree
        heapify(arr, n, largest)


def heap_sort(arr: List[int]) -> List[int]:
    """
    Performs Heap Sort in-place on arr and returns it.
    """
    n = len(arr)

    # 1. Build a maxheap (start from last non-leaf node down to 0)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # 2. Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        # Move current root (largest) to end
        arr[i], arr[0] = arr[0], arr[i]
        # Call max heapify on the reduced heap
        heapify(arr, i, 0)

    return arr


def heap_sort_traced(arr: List[int]) -> List[int]:
    """
    Heap sort with step-by-step console outputs.
    """
    a = arr.copy()
    n = len(a)
    print(f"\nInitial Array: {a}")
    print("-" * 60)

    # Build max heap
    print("Building Max-Heap:")
    for i in range(n // 2 - 1, -1, -1):
        heapify(a, n, i)
        print(f"  After heapify at index {i}: {a}")

    print(f"\nMax-Heap Created: {a}")
    print("-" * 60)
    print("Extracting elements one by one:")

    for i in range(n - 1, 0, -1):
        a[i], a[0] = a[0], a[i]
        print(f"Swapped max ({a[i]}) to index {i} -> {a}")
        heapify(a, i, 0)
        print(f"  Heapified root (heap size {i}) -> {a}")

    print("-" * 60)
    print(f"Final Sorted Array: {a}\n")
    return a


if __name__ == "__main__":
    print("=" * 60)
    print("        COLLEGE DSA LAB: HEAP SORT")
    print("=" * 60)

    sample = [12, 11, 13, 5, 6, 7]
    heap_sort_traced(sample)
