"""
Experiment: Priority Queue ADT (Binary Heap Based)
---------------------------------------------------
Aim:
    To implement a Priority Queue using a Binary Min-Heap and Max-Heap,
    demonstrating efficient insertion, highest priority extraction,
    and priority updates.

Theory:
    A Priority Queue is an extension of a queue with following properties:
    - Every item has a priority associated with it.
    - An element with high priority is dequeued before an element with low priority.
    - If two elements have the same priority, they are served according to their order in the queue.
    
    A Binary Heap is the ideal underlying data structure for a Priority Queue:
    - Insert: O(log n)
    - Extract-Min/Max: O(log n)
    - Peek (Get Min/Max): O(1)
"""

from typing import Any, List, Optional, Tuple


class PriorityQueueElement:
    def __init__(self, item: Any, priority: int):
        self.item = item
        self.priority = priority

    def __repr__(self):
        return f"({self.item}, priority={self.priority})"


class MinPriorityQueue:
    """
    Min-Priority Queue: Lower priority integer means higher service priority (e.g., Priority 1 before Priority 5).
    """
    def __init__(self):
        self.heap: List[PriorityQueueElement] = []

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    def size(self) -> int:
        return len(self.heap)

    def insert(self, item: Any, priority: int) -> None:
        """Inserts an item with given priority in O(log n)."""
        elem = PriorityQueueElement(item, priority)
        self.heap.append(elem)
        self._sift_up(len(self.heap) - 1)

    def extract_min(self) -> Any:
        """Removes and returns the item with minimum priority value (highest priority)."""
        if self.is_empty():
            raise IndexError("Cannot extract from empty Priority Queue.")

        root = self.heap[0]
        last = self.heap.pop()

        if self.heap:
            self.heap[0] = last
            self._sift_down(0)

        return root.item

    def peek(self) -> Any:
        """Returns the highest-priority item without removing it."""
        if self.is_empty():
            raise IndexError("Priority Queue is empty.")
        return self.heap[0].item

    def _sift_up(self, index: int) -> None:
        parent = (index - 1) // 2
        while index > 0 and self.heap[index].priority < self.heap[parent].priority:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent
            parent = (index - 1) // 2

    def _sift_down(self, index: int) -> None:
        n = len(self.heap)
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < n and self.heap[left].priority < self.heap[smallest].priority:
            smallest = left
        if right < n and self.heap[right].priority < self.heap[smallest].priority:
            smallest = right

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._sift_down(smallest)

    def display(self) -> None:
        if self.is_empty():
            print("Priority Queue is EMPTY.")
            return
        print("Priority Queue (Heap): " + " -> ".join(str(e) for e in self.heap))


if __name__ == "__main__":
    print("=" * 60)
    print("        COLLEGE DSA LAB: PRIORITY QUEUE")
    print("=" * 60)

    pq = MinPriorityQueue()
    tasks = [
        ("Emergency Patient", 1),
        ("Routine Checkup", 4),
        ("Urgent Consultation", 2),
        ("Follow-up Visit", 5),
        ("Lab Results Review", 3),
    ]

    print("Inserting tasks with priorities:")
    for task, prio in tasks:
        pq.insert(task, prio)
        print(f"  Inserted: '{task}' with Priority {prio}")

    print("\nCurrent Heap Structure:")
    pq.display()

    print("\nProcessing/Extracting in priority order:")
    while not pq.is_empty():
        print(f"  Serving: {pq.extract_min()}")
