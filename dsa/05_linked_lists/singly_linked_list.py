"""
Experiment: Singly Linked List Operations
------------------------------------------
Aim:
    To implement a comprehensive Singly Linked List data structure in Python,
    supporting insertion, deletion, searching, reversing (iterative & recursive),
    cycle detection (Floyd's Tortoise and Hare algorithm), and merging sorted lists.

Theory:
    A Singly Linked List is a linear data structure consisting of nodes where
    each node contains data and a pointer/reference to the next node in the
    sequence. Unlike arrays, linked list elements are not stored at contiguous
    memory locations.

Operations & Complexities:
    - Insert at Head:           O(1)
    - Insert at Tail:           O(n) (or O(1) with tail pointer)
    - Insert at Position:       O(n)
    - Delete Head:              O(1)
    - Delete Tail:              O(n)
    - Delete by Value:          O(n)
    - Search:                   O(n)
    - Reverse List:             O(n) time, O(1) space
    - Detect Loop (Floyd's):    O(n) time, O(1) space
"""

from typing import Any, List, Optional


class Node:
    """Represents a singly linked list node."""
    def __init__(self, data: Any):
        self.data: Any = data
        self.next: Optional["Node"] = None

    def __repr__(self):
        return f"Node({self.data})"


class SinglyLinkedList:
    """
    Singly Linked List with all standard university lab operations.
    """
    def __init__(self):
        self.head: Optional[Node] = None

    def insert_at_beginning(self, data: Any) -> None:
        """Inserts a new node at the head of the list. O(1)"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data: Any) -> None:
        """Inserts a new node at the tail of the list. O(n)"""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    def insert_at_index(self, index: int, data: Any) -> None:
        """Inserts a node at a 0-based index."""
        if index < 0:
            raise IndexError("Negative index not supported.")
        if index == 0:
            self.insert_at_beginning(data)
            return

        curr = self.head
        for _ in range(index - 1):
            if curr is None:
                raise IndexError("Index out of bounds.")
            curr = curr.next

        if curr is None:
            raise IndexError("Index out of bounds.")

        new_node = Node(data)
        new_node.next = curr.next
        curr.next = new_node

    def delete_at_beginning(self) -> Any:
        """Deletes the head node and returns its data. O(1)"""
        if self.head is None:
            raise IndexError("Cannot delete from empty linked list.")
        val = self.head.data
        self.head = self.head.next
        return val

    def delete_at_end(self) -> Any:
        """Deletes the tail node and returns its data. O(n)"""
        if self.head is None:
            raise IndexError("Cannot delete from empty linked list.")
        if self.head.next is None:
            val = self.head.data
            self.head = None
            return val

        curr = self.head
        while curr.next and curr.next.next:
            curr = curr.next
        assert curr.next is not None
        val = curr.next.data
        curr.next = None
        return val

    def delete_by_value(self, key: Any) -> bool:
        """Deletes the first occurrence of key. Returns True if found, else False."""
        if self.head is None:
            return False

        if self.head.data == key:
            self.head = self.head.next
            return True

        curr = self.head
        while curr.next and curr.next.data != key:
            curr = curr.next

        if curr.next is None:
            return False  # Key not found

        curr.next = curr.next.next
        return True

    def search(self, key: Any) -> int:
        """Searches for key and returns its 0-based index, or -1 if not found."""
        curr = self.head
        idx = 0
        while curr:
            if curr.data == key:
                return idx
            curr = curr.next
            idx += 1
        return -1

    def reverse_iterative(self) -> None:
        """Reverses the list in-place iteratively using 3 pointers. O(n) time, O(1) space."""
        prev = None
        curr = self.head
        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node
        self.head = prev

    def reverse_recursive(self) -> None:
        """Reverses the list in-place recursively."""
        def _rev(curr: Optional[Node], prev: Optional[Node]) -> Optional[Node]:
            if curr is None:
                return prev
            next_node = curr.next
            curr.next = prev
            return _rev(next_node, curr)

        self.head = _rev(self.head, None)

    def detect_and_remove_loop(self) -> bool:
        """
        Detects loop using Floyd's Cycle-Finding Algorithm (Tortoise and Hare).
        If a loop exists, breaks the cycle and returns True; otherwise False.
        """
        if self.head is None or self.head.next is None:
            return False

        slow = self.head
        fast = self.head

        # Phase 1: Detection
        loop_found = False
        while fast and fast.next:
            slow = slow.next  # type: ignore
            fast = fast.next.next
            if slow == fast:
                loop_found = True
                break

        if not loop_found:
            return False

        # Phase 2: Find start of loop and break it
        slow = self.head
        if slow == fast:
            # Special case: loop starts at head
            while fast.next != slow:  # type: ignore
                fast = fast.next  # type: ignore
            fast.next = None  # type: ignore
            return True

        while slow.next != fast.next:  # type: ignore
            slow = slow.next  # type: ignore
            fast = fast.next  # type: ignore

        # fast.next is the start of the loop
        fast.next = None  # type: ignore
        return True

    def to_list(self) -> List[Any]:
        """Converts linked list into a Python list."""
        res = []
        curr = self.head
        while curr:
            res.append(curr.data)
            curr = curr.next
        return res

    def display(self) -> None:
        """Displays the linked list."""
        if self.head is None:
            print("List is EMPTY: [None]")
            return
        items = [f"[{node_data}]" for node_data in self.to_list()]
        print("HEAD -> " + " -> ".join(items) + " -> None")


def merge_two_sorted_lists(l1: SinglyLinkedList, l2: SinglyLinkedList) -> SinglyLinkedList:
    """
    Merges two sorted Singly Linked Lists into a new sorted Singly Linked List in O(n + m).
    """
    merged = SinglyLinkedList()
    dummy = Node(0)
    tail = dummy

    p1 = l1.head
    p2 = l2.head

    while p1 and p2:
        if p1.data <= p2.data:
            tail.next = Node(p1.data)
            p1 = p1.next
        else:
            tail.next = Node(p2.data)
            p2 = p2.next
        tail = tail.next

    while p1:
        tail.next = Node(p1.data)
        p1 = p1.next
        tail = tail.next

    while p2:
        tail.next = Node(p2.data)
        p2 = p2.next
        tail = tail.next

    merged.head = dummy.next
    return merged


if __name__ == "__main__":
    print("=" * 65)
    print("        COLLEGE DSA LAB: SINGLY LINKED LIST EXPERIMENT")
    print("=" * 65)

    sll = SinglyLinkedList()

    # Insertions
    sll.insert_at_beginning(30)
    sll.insert_at_beginning(10)
    sll.insert_at_end(50)
    sll.insert_at_index(1, 20)  # Insert 20 between 10 and 30
    sll.insert_at_index(3, 40)  # Insert 40 between 30 and 50
    print("Initial List after insertions:")
    sll.display()

    # Deletions
    print(f"\nDeleted head: {sll.delete_at_beginning()}")
    sll.display()
    print(f"Deleted tail: {sll.delete_at_end()}")
    sll.display()
    print(f"Delete value 30: {sll.delete_by_value(30)}")
    sll.display()

    # Reversal
    sll.insert_at_beginning(5)
    sll.insert_at_end(99)
    print("\nBefore reversal:")
    sll.display()
    sll.reverse_iterative()
    print("After iterative reversal:")
    sll.display()
    sll.reverse_recursive()
    print("After recursive reversal (back to original):")
    sll.display()

    # Merge Two Sorted Lists
    list_a = SinglyLinkedList()
    for x in [1, 3, 5, 7]:
        list_a.insert_at_end(x)
    list_b = SinglyLinkedList()
    for y in [2, 4, 6, 8]:
        list_b.insert_at_end(y)

    print("\nMerging two sorted lists:")
    print("List A: ", end="")
    list_a.display()
    print("List B: ", end="")
    list_b.display()
    merged = merge_two_sorted_lists(list_a, list_b)
    print("Merged: ", end="")
    merged.display()

    # Cycle Detection
    print("\nTesting Floyd's Loop Detection and Removal:")
    loop_list = SinglyLinkedList()
    for v in [100, 200, 300, 400, 500]:
        loop_list.insert_at_end(v)

    # Artificially create cycle: 500 -> 300
    n500 = loop_list.head
    while n500.next:
        n500 = n500.next
    n300 = loop_list.head.next.next  # node with 300
    n500.next = n300

    print("Cycle created (500 -> 300).")
    detected = loop_list.detect_and_remove_loop()
    print(f"Loop detected and removed: {detected}")
    loop_list.display()
