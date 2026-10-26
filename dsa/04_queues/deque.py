"""
Experiment: Double-Ended Queue (Deque ADT)
-------------------------------------------
Aim:
    To implement a Double-Ended Queue (Deque) using a circular array, supporting
    insertion and deletion at both ends, and discuss input-restricted vs
    output-restricted variations.

Theory:
    A Deque (Double Ended Queue) is a generalized queue where elements can be
    added or removed from either the front or the rear.
    
    Types of Deques:
    1. Input-Restricted Deque: Insertion is allowed at one end only (rear),
       while deletion is allowed at both ends.
    2. Output-Restricted Deque: Deletion is allowed at one end only (front),
       while insertion is allowed at both ends.

Operations:
    - insert_front(x)
    - insert_rear(x)
    - delete_front()
    - delete_rear()
    - get_front(), get_rear()

Time Complexity:
    - All operations run in O(1) time.
"""

from typing import Any, List


class Deque:
    """
    Circular Array implementation of Double-Ended Queue (Deque).
    """
    def __init__(self, capacity: int = 6):
        self.capacity = capacity
        self.arr: List[Any] = [None] * capacity
        self.front = -1
        self.rear = -1

    def is_empty(self) -> bool:
        return self.front == -1

    def is_full(self) -> bool:
        return (self.front == 0 and self.rear == self.capacity - 1) or (self.front == self.rear + 1)

    def insert_front(self, item: Any) -> None:
        if self.is_full():
            raise OverflowError(f"Deque Overflow! Cannot insert {item} at front.")

        if self.front == -1:  # First element
            self.front = self.rear = 0
        elif self.front == 0:
            self.front = self.capacity - 1
        else:
            self.front -= 1

        self.arr[self.front] = item

    def insert_rear(self, item: Any) -> None:
        if self.is_full():
            raise OverflowError(f"Deque Overflow! Cannot insert {item} at rear.")

        if self.front == -1:  # First element
            self.front = self.rear = 0
        elif self.rear == self.capacity - 1:
            self.rear = 0
        else:
            self.rear += 1

        self.arr[self.rear] = item

    def delete_front(self) -> Any:
        if self.is_empty():
            raise IndexError("Deque Underflow! Cannot delete from front.")

        item = self.arr[self.front]
        self.arr[self.front] = None

        if self.front == self.rear:
            self.front = self.rear = -1
        elif self.front == self.capacity - 1:
            self.front = 0
        else:
            self.front += 1

        return item

    def delete_rear(self) -> Any:
        if self.is_empty():
            raise IndexError("Deque Underflow! Cannot delete from rear.")

        item = self.arr[self.rear]
        self.arr[self.rear] = None

        if self.front == self.rear:
            self.front = self.rear = -1
        elif self.rear == 0:
            self.rear = self.capacity - 1
        else:
            self.rear -= 1

        return item

    def get_front(self) -> Any:
        if self.is_empty():
            raise IndexError("Deque is empty.")
        return self.arr[self.front]

    def get_rear(self) -> Any:
        if self.is_empty():
            raise IndexError("Deque is empty.")
        return self.arr[self.rear]

    def display(self) -> None:
        if self.is_empty():
            print("Deque is EMPTY.")
            return
        print(f"Internal Buffer: {self.arr} (Front={self.front}, Rear={self.rear})")


if __name__ == "__main__":
    print("=" * 60)
    print("        COLLEGE DSA LAB: DOUBLE-ENDED QUEUE (DEQUE)")
    print("=" * 60)

    dq = Deque(capacity=5)
    dq.insert_rear(10)
    dq.insert_rear(20)
    dq.insert_front(5)
    dq.insert_front(1)
    dq.display()

    print(f"Deleted Front: {dq.delete_front()}")
    print(f"Deleted Rear:  {dq.delete_rear()}")
    dq.display()
