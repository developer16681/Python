"""
Experiment: Stack ADT using Linked List
----------------------------------------
Aim:
    To implement a dynamic Stack data structure using Singly Linked List nodes,
    eliminating fixed-capacity restrictions while retaining O(1) push and pop.

Theory:
    In a linked list representation of a stack:
    - Nodes are dynamically allocated on the heap.
    - The 'top' pointer points to the head node of the list.
    - 'push' inserts a new node before the current head and updates 'top'.
    - 'pop' removes the head node and advances 'top' to the next node.
    - Stack overflow only occurs if the system runs out of physical memory.

Time Complexity:
    - push():     O(1)
    - pop():      O(1)
    - peek():     O(1)
    - is_empty(): O(1)

Space Complexity:
    - O(n) where each element has pointer overhead (data + next pointer).
"""

from typing import Any, Optional


class StackNode:
    """Represents an individual node in the linked stack."""
    def __init__(self, data: Any):
        self.data: Any = data
        self.next: Optional["StackNode"] = None


class LinkedListStack:
    """
    Dynamic Stack implemented using a Singly Linked List.
    """
    def __init__(self):
        self._top: Optional[StackNode] = None
        self._size: int = 0

    def push(self, data: Any) -> None:
        """Pushes data onto the top of the stack."""
        new_node = StackNode(data)
        new_node.next = self._top
        self._top = new_node
        self._size += 1

    def pop(self) -> Any:
        """Pops and returns the top element. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("Cannot pop from an empty linked stack.")
        assert self._top is not None
        popped_val = self._top.data
        self._top = self._top.next
        self._size -= 1
        return popped_val

    def peek(self) -> Any:
        """Returns the top element without removing it."""
        if self.is_empty():
            raise IndexError("Cannot peek into an empty linked stack.")
        assert self._top is not None
        return self._top.data

    def is_empty(self) -> bool:
        """Checks if the stack is empty."""
        return self._top is None

    def size(self) -> int:
        """Returns the count of items in the stack."""
        return self._size

    def display(self) -> None:
        """Visualizes the linked list stack chain."""
        if self.is_empty():
            print("Stack is EMPTY: [None]")
            return

        nodes = []
        curr = self._top
        while curr:
            nodes.append(f"[{curr.data}]")
            curr = curr.next

        print("TOP -> " + " -> ".join(nodes) + " -> None")


if __name__ == "__main__":
    print("=" * 60)
    print("     COLLEGE DSA LAB: STACK USING LINKED LIST")
    print("=" * 60)

    s = LinkedListStack()
    for item in ["Apple", "Banana", "Cherry", "Date"]:
        s.push(item)
        print(f"Pushed: {item:<6} | Size: {s.size()}")

    print("\nVisual representation:")
    s.display()

    print(f"\nTop element: {s.peek()}")
    print(f"Popped: {s.pop()}")
    print(f"Popped: {s.pop()}")

    print("\nAfter popping two elements:")
    s.display()
    print(f"Current Size: {s.size()}")
