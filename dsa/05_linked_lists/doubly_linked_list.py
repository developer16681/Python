"""
Experiment: Doubly Linked List Operations
------------------------------------------
Aim:
    To implement a Doubly Linked List (DLL) in Python, demonstrating bidirectional
    traversal, insertion, and deletion at any position using prev and next pointers.

Theory:
    A Doubly Linked List contains nodes with three fields:
    1. Data
    2. Pointer to previous node (prev)
    3. Pointer to next node (next)
    
    Advantages over Singly Linked List:
    - Can be traversed in both forward and backward directions.
    - Deletion of a given node is O(1) if pointer to that node is given
      (no need to traverse to find the predecessor).

Time Complexity:
    - Insert Head / Tail: O(1) (with tail pointer)
    - Delete Head / Tail: O(1)
    - Forward / Backward Traversal: O(n)
"""

from typing import Any, List, Optional


class DNode:
    """Doubly linked list node."""
    def __init__(self, data: Any):
        self.data: Any = data
        self.prev: Optional["DNode"] = None
        self.next: Optional["DNode"] = None

    def __repr__(self):
        return f"DNode({self.data})"


class DoublyLinkedList:
    """
    Doubly Linked List implementation with head and tail pointers.
    """
    def __init__(self):
        self.head: Optional[DNode] = None
        self.tail: Optional[DNode] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        return self.head is None

    def insert_at_head(self, data: Any) -> None:
        """Inserts a new node at the front. O(1)"""
        new_node = DNode(data)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._size += 1

    def insert_at_tail(self, data: Any) -> None:
        """Inserts a new node at the end. O(1)"""
        new_node = DNode(data)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self._size += 1

    def delete_head(self) -> Any:
        """Removes the front node. O(1)"""
        if self.is_empty():
            raise IndexError("Cannot delete from empty doubly linked list.")
        val = self.head.data
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        self._size -= 1
        return val

    def delete_tail(self) -> Any:
        """Removes the tail node. O(1)"""
        if self.is_empty():
            raise IndexError("Cannot delete from empty doubly linked list.")
        val = self.tail.data
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        self._size -= 1
        return val

    def display_forward(self) -> None:
        """Traverses and prints from head to tail."""
        if self.is_empty():
            print("Forward Traversal: [None]")
            return
        elements = []
        curr = self.head
        while curr:
            elements.append(f"[{curr.data}]")
            curr = curr.next
        print("HEAD <-> " + " <-> ".join(elements) + " <-> TAIL")

    def display_backward(self) -> None:
        """Traverses and prints from tail to head."""
        if self.is_empty():
            print("Backward Traversal: [None]")
            return
        elements = []
        curr = self.tail
        while curr:
            elements.append(f"[{curr.data}]")
            curr = curr.prev
        print("TAIL <-> " + " <-> ".join(elements) + " <-> HEAD")


if __name__ == "__main__":
    print("=" * 65)
    print("        COLLEGE DSA LAB: DOUBLY LINKED LIST")
    print("=" * 65)

    dll = DoublyLinkedList()

    # Insertions
    dll.insert_at_tail(20)
    dll.insert_at_tail(30)
    dll.insert_at_head(10)
    dll.insert_at_tail(40)
    dll.insert_at_head(5)

    print("List after insertions:")
    dll.display_forward()
    dll.display_backward()

    # Deletions
    print(f"\nDeleted Head: {dll.delete_head()}")
    print(f"Deleted Tail: {dll.delete_tail()}")

    print("\nList after deletions:")
    dll.display_forward()
    dll.display_backward()
