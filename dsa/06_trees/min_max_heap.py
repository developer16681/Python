"""
Experiment: Min-Heap and Max-Heap Operations
---------------------------------------------
Aim:
    To implement Binary Min-Heap and Max-Heap data structures from scratch
    using an array representation, including heapify, insertion, and root extraction.

Theory:
    A Binary Heap is a complete binary tree which satisfies the heap property:
    - Min-Heap: For every node i, value(parent(i)) <= value(i). Root is minimum.
    - Max-Heap: For every node i, value(parent(i)) >= value(i). Root is maximum.

Array Representation:
    For a node at 0-based index i:
    - Left Child:  2 * i + 1
    - Right Child: 2 * i + 2
    - Parent:      (i - 1) // 2

Time Complexity:
    - Insert:      O(log n) (Sift up)
    - Extract Root: O(log n) (Sift down)
    - Peek Root:   O(1)
    - Build Heap:  O(n)
"""

from typing import Any, List, Optional


class MinHeap:
    def __init__(self):
        self.heap: List[int] = []

    def parent(self, i: int) -> int:
        return (i - 1) // 2

    def left_child(self, i: int) -> int:
        return 2 * i + 1

    def right_child(self, i: int) -> int:
        return 2 * i + 2

    def insert(self, key: int) -> None:
        self.heap.append(key)
        self._sift_up(len(self.heap) - 1)

    def extract_min(self) -> int:
        if not self.heap:
            raise IndexError("Heap is empty.")
        min_val = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._sift_down(0)
        return min_val

    def peek(self) -> int:
        if not self.heap:
            raise IndexError("Heap is empty.")
        return self.heap[0]

    def _sift_up(self, i: int) -> None:
        while i > 0 and self.heap[i] < self.heap[self.parent(i)]:
            p = self.parent(i)
            self.heap[i], self.heap[p] = self.heap[p], self.heap[i]
            i = p

    def _sift_down(self, i: int) -> None:
        n = len(self.heap)
        smallest = i
        left = self.left_child(i)
        right = self.right_child(i)

        if left < n and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < n and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self._sift_down(smallest)

    def display(self) -> None:
        print(f"Min-Heap Array: {self.heap}")


class MaxHeap:
    def __init__(self):
        self.heap: List[int] = []

    def parent(self, i: int) -> int:
        return (i - 1) // 2

    def left_child(self, i: int) -> int:
        return 2 * i + 1

    def right_child(self, i: int) -> int:
        return 2 * i + 2

    def insert(self, key: int) -> None:
        self.heap.append(key)
        self._sift_up(len(self.heap) - 1)

    def extract_max(self) -> int:
        if not self.heap:
            raise IndexError("Heap is empty.")
        max_val = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._sift_down(0)
        return max_val

    def peek(self) -> int:
        if not self.heap:
            raise IndexError("Heap is empty.")
        return self.heap[0]

    def _sift_up(self, i: int) -> None:
        while i > 0 and self.heap[i] > self.heap[self.parent(i)]:
            p = self.parent(i)
            self.heap[i], self.heap[p] = self.heap[p], self.heap[i]
            i = p

    def _sift_down(self, i: int) -> None:
        n = len(self.heap)
        largest = i
        left = self.left_child(i)
        right = self.right_child(i)

        if left < n and self.heap[left] > self.heap[largest]:
            largest = left
        if right < n and self.heap[right] > self.heap[largest]:
            largest = right

        if largest != i:
            self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
            self._sift_down(largest)

    def display(self) -> None:
        print(f"Max-Heap Array: {self.heap}")


if __name__ == "__main__":
    print("=" * 65)
    print("        COLLEGE DSA LAB: MIN-HEAP & MAX-HEAP")
    print("=" * 65)

    data = [40, 20, 30, 10, 50, 15]
    print(f"Raw Input: {data}\n")

    # Min Heap
    min_h = MinHeap()
    for x in data:
        min_h.insert(x)
    print("--- Min-Heap Test ---")
    min_h.display()
    print(f"Peek Min: {min_h.peek()}")
    print("Extracting elements in ascending order:")
    while min_h.heap:
        print(min_h.extract_min(), end=" ")
    print("\n")

    # Max Heap
    max_h = MaxHeap()
    for x in data:
        max_h.insert(x)
    print("--- Max-Heap Test ---")
    max_h.display()
    print(f"Peek Max: {max_h.peek()}")
    print("Extracting elements in descending order:")
    while max_h.heap:
        print(max_h.extract_max(), end=" ")
    print()
