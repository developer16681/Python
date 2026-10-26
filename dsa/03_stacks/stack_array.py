"""
Experiment: Stack ADT Implementation using Array / List
-------------------------------------------------------
Aim:
    To implement the Stack Abstract Data Type (ADT) using a fixed-capacity array
    in Python, demonstrating LIFO (Last-In-First-Out) operations with overflow
    and underflow exception handling.

Theory:
    A stack is a linear data structure following the LIFO (Last In First Out)
    or FILO (First In Last Out) principle. Operations are performed only at
    one end called the 'top'.
    
    Primary Operations:
    - push(element): Insert an item onto the top of the stack.
    - pop(): Remove and return the top item.
    - peek() / top(): View the top item without removing it.
    - is_empty(): Check whether the stack contains any items.
    - is_full(): Check whether the stack has reached maximum capacity.
    - size(): Return total number of items in the stack.

Time Complexity:
    - push():     O(1)
    - pop():      O(1)
    - peek():     O(1)
    - is_empty(): O(1)
    - is_full():  O(1)

Space Complexity:
    - O(n) where n is capacity of the stack.
"""

from typing import Any, List, Optional


class StackOverflowError(Exception):
    """Exception raised when pushing onto a full stack."""
    pass


class StackUnderflowError(Exception):
    """Exception raised when popping or peeking from an empty stack."""
    pass


class ArrayStack:
    """
    Fixed-capacity Stack ADT implementation.
    """
    def __init__(self, capacity: int = 10):
        if capacity <= 0:
            raise ValueError("Stack capacity must be positive.")
        self.capacity = capacity
        self._items: List[Any] = [None] * capacity
        self._top = -1  # Points to the top element index

    def push(self, item: Any) -> None:
        """Adds an item to the top of stack. Raises StackOverflowError if full."""
        if self.is_full():
            raise StackOverflowError(f"Stack Overflow! Cannot push {item}. Capacity of {self.capacity} reached.")
        self._top += 1
        self._items[self._top] = item

    def pop(self) -> Any:
        """Removes and returns top item. Raises StackUnderflowError if empty."""
        if self.is_empty():
            raise StackUnderflowError("Stack Underflow! Cannot pop from empty stack.")
        item = self._items[self._top]
        self._items[self._top] = None  # Clear reference
        self._top -= 1
        return item

    def peek(self) -> Any:
        """Returns top item without removing. Raises StackUnderflowError if empty."""
        if self.is_empty():
            raise StackUnderflowError("Stack is empty. Cannot peek.")
        return self._items[self._top]

    def is_empty(self) -> bool:
        """Returns True if stack has no elements."""
        return self._top == -1

    def is_full(self) -> bool:
        """Returns True if stack has reached its maximum capacity."""
        return self._top == self.capacity - 1

    def size(self) -> int:
        """Returns current number of elements."""
        return self._top + 1

    def display(self) -> None:
        """Displays stack contents from top to bottom."""
        if self.is_empty():
            print("Stack is EMPTY [ ]")
            return

        print(f"\n--- Stack Contents (Size {self.size()}/{self.capacity}) ---")
        for i in range(self._top, -1, -1):
            marker = " <-- TOP" if i == self._top else ""
            print(f"| {self._items[i]:^8} |{marker}")
        print("+" + "-" * 10 + "+")


if __name__ == "__main__":
    print("=" * 60)
    print("        COLLEGE DSA LAB: STACK ADT (ARRAY BASED)")
    print("=" * 60)

    stack = ArrayStack(capacity=5)
    print(f"Created stack with capacity {stack.capacity}.")

    # Push operations
    for val in [10, 20, 30, 40]:
        stack.push(val)
        print(f"Pushed {val} | Current Top: {stack.peek()} | Size: {stack.size()}")

    stack.display()

    print(f"\nPeek element: {stack.peek()}")
    print(f"Popped element: {stack.pop()}")
    print(f"Popped element: {stack.pop()}")

    stack.display()

    # Fill to capacity
    stack.push(50)
    stack.push(60)
    stack.push(70)
    stack.display()

    # Test overflow
    try:
        print("Attempting to push 80 into full stack:")
        stack.push(80)
    except StackOverflowError as e:
        print(f"Caught expected error: {e}")

    # Empty stack completely
    while not stack.is_empty():
        print(f"Popped: {stack.pop()}")

    # Test underflow
    try:
        print("Attempting to pop from empty stack:")
        stack.pop()
    except StackUnderflowError as e:
        print(f"Caught expected error: {e}")
