"""
Experiment: Circular Queue ADT
-------------------------------
Aim:
    To implement a Circular Queue using an array in Python and demonstrate how
    modulo arithmetic prevents memory wastage inherent to linear queues.

Theory:
    In a standard linear queue implemented using an array, once the rear pointer
    reaches the end of the array, no further insertions can be made even if
    empty spaces exist at the front due to dequeues.
    A Circular Queue overcomes this by wrapping around to the beginning using
    modulo arithmetic:
        next_rear = (rear + 1) % capacity
        next_front = (front + 1) % capacity
        
    Queue Full Condition:
        (rear + 1) % capacity == front
    Queue Empty Condition:
        front == -1

Time Complexity:
    - enqueue(): O(1)
    - dequeue(): O(1)
    - peek():    O(1)

Space Complexity:
    - O(n) fixed capacity array.
"""

from typing import Any, List


class CircularQueue:
    """
    Circular Queue implementation using a fixed array.
    """
    def __init__(self, capacity: int = 5):
        if capacity <= 0:
            raise ValueError("Capacity must be positive.")
        self.capacity = capacity
        self.queue: List[Any] = [None] * capacity
        self.front = -1
        self.rear = -1

    def is_empty(self) -> bool:
        return self.front == -1

    def is_full(self) -> bool:
        return (self.rear + 1) % self.capacity == self.front

    def enqueue(self, item: Any) -> None:
        if self.is_full():
            raise OverflowError(f"Circular Queue Overflow! Cannot insert {item}.")

        if self.front == -1:  # First element insertion
            self.front = 0
            self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.capacity

        self.queue[self.rear] = item

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("Circular Queue Underflow! Queue is empty.")

        item = self.queue[self.front]
        self.queue[self.front] = None

        if self.front == self.rear:
            # Only one element was present, reset to empty state
            self.front = -1
            self.rear = -1
        else:
            self.front = (self.front + 1) % self.capacity

        return item

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("Queue is empty.")
        return self.queue[self.front]

    def display(self) -> None:
        if self.is_empty():
            print("Circular Queue is EMPTY [ ]")
            return

        print(f"\nInternal Array: {self.queue} | Front: {self.front}, Rear: {self.rear}")
        print("Queue Sequence: ", end="")
        i = self.front
        items = []
        while True:
            items.append(str(self.queue[i]))
            if i == self.rear:
                break
            i = (i + 1) % self.capacity
        print(" -> ".join(items))


if __name__ == "__main__":
    print("=" * 60)
    print("        COLLEGE DSA LAB: CIRCULAR QUEUE")
    print("=" * 60)

    cq = CircularQueue(capacity=5)

    # Insert 4 items
    for val in [10, 20, 30, 40]:
        cq.enqueue(val)
    cq.display()

    # Dequeue 2 items (frees slots at beginning)
    print(f"\nDequeued: {cq.dequeue()}")
    print(f"Dequeued: {cq.dequeue()}")
    cq.display()

    # Enqueue more elements to verify wrap-around to index 0, 1
    print("\nEnqueueing 50, 60, 70 to demonstrate wrap-around:")
    cq.enqueue(50)
    cq.enqueue(60)
    cq.enqueue(70)
    cq.display()

    # Test queue full condition
    try:
        print("Attempting to enqueue 80 into full circular queue:")
        cq.enqueue(80)
    except OverflowError as e:
        print(f"Caught: {e}")
