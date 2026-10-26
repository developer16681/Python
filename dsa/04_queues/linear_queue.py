"""
Experiment: Linear Queue ADT (Array and Linked List Implementations)
---------------------------------------------------------------------
Aim:
    To implement the Linear Queue Abstract Data Type (ADT) using both a fixed
    array and a linked list, demonstrating FIFO (First-In-First-Out) behavior.

Theory:
    A Queue is a linear data structure that follows the FIFO (First In First Out)
    principle. Insertion happens at the 'rear' and removal happens at the 'front'.
    
    Primary Operations:
    - enqueue(item): Add an element to the rear of the queue.
    - dequeue(): Remove and return the front element of the queue.
    - peek(): View the front element without removing it.
    - is_empty(): Test if queue contains elements.
    - is_full(): Test if queue reached fixed limit (for array-based queue).

Time Complexity:
    - Array Queue:
        - enqueue(): O(1)
        - dequeue(): O(1) with sliding front pointer, or O(n) if shifting.
    - Linked Queue:
        - enqueue(): O(1)
        - dequeue(): O(1)
"""

from typing import Any, List, Optional


class ArrayLinearQueue:
    """
    Fixed-capacity Linear Queue using two pointers (front and rear).
    """
    def __init__(self, capacity: int = 5):
        self.capacity = capacity
        self.arr: List[Any] = [None] * capacity
        self.front = -1
        self.rear = -1

    def is_empty(self) -> bool:
        return self.front == -1 or self.front > self.rear

    def is_full(self) -> bool:
        return self.rear == self.capacity - 1

    def enqueue(self, item: Any) -> None:
        if self.is_full():
            raise OverflowError(f"Queue Overflow! Cannot enqueue {item}.")
        if self.front == -1:
            self.front = 0
        self.rear += 1
        self.arr[self.rear] = item

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("Queue Underflow! Cannot dequeue from empty queue.")
        item = self.arr[self.front]
        self.arr[self.front] = None
        self.front += 1
        if self.front > self.rear:  # Reset when queue becomes empty
            self.front = self.rear = -1
        return item

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("Queue is empty. Cannot peek.")
        return self.arr[self.front]

    def display(self) -> None:
        if self.is_empty():
            print("Queue is EMPTY.")
            return
        items = [str(self.arr[i]) for i in range(self.front, self.rear + 1)]
        print(f"FRONT [{self.front}] -> " + " -> ".join(items) + f" <- REAR [{self.rear}]")


class QueueNode:
    def __init__(self, data: Any):
        self.data = data
        self.next: Optional["QueueNode"] = None


class LinkedQueue:
    """
    Dynamic Queue implemented using a Singly Linked List with head and tail pointers.
    """
    def __init__(self):
        self._front: Optional[QueueNode] = None
        self._rear: Optional[QueueNode] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        return self._front is None

    def enqueue(self, data: Any) -> None:
        new_node = QueueNode(data)
        if self._rear is None:
            self._front = self._rear = new_node
        else:
            self._rear.next = new_node
            self._rear = new_node
        self._size += 1

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("Queue Underflow! Cannot dequeue from empty linked queue.")
        assert self._front is not None
        val = self._front.data
        self._front = self._front.next
        if self._front is None:
            self._rear = None
        self._size -= 1
        return val

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("Queue is empty.")
        assert self._front is not None
        return self._front.data

    def display(self) -> None:
        if self.is_empty():
            print("Linked Queue is EMPTY.")
            return
        nodes = []
        curr = self._front
        while curr:
            nodes.append(f"[{curr.data}]")
            curr = curr.next
        print("FRONT -> " + " -> ".join(nodes) + " <- REAR")


if __name__ == "__main__":
    print("=" * 60)
    print("        COLLEGE DSA LAB: LINEAR QUEUE EXPERIMENT")
    print("=" * 60)

    # 1. Array Linear Queue
    print("--- Array-Based Linear Queue ---")
    aq = ArrayLinearQueue(capacity=4)
    for v in [10, 20, 30]:
        aq.enqueue(v)
    aq.display()

    print(f"Dequeued: {aq.dequeue()}")
    aq.display()

    aq.enqueue(40)
    aq.display()

    # 2. Linked Queue
    print("\n--- Linked-List-Based Dynamic Queue ---")
    lq = LinkedQueue()
    for task in ["Job A", "Job B", "Job C"]:
        lq.enqueue(task)
    lq.display()
    print(f"Servicing: {lq.dequeue()}")
    lq.display()
