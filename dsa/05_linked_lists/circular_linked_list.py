"""
Experiment: Circular Singly Linked List Operations
---------------------------------------------------
Aim:
    To implement a Circular Singly Linked List (CSLL) in Python, where the last
    node points back to the head node, and demonstrate operations such as
    insertion, deletion, circular traversal, and splitting into two halves.

Theory:
    A circular linked list is a sequence of elements in which every element has
    a link to its next element in the sequence and the last element has a link
    to the first element. There is no NULL at the end.
    
    Using a 'last' (tail) pointer allows O(1) insertion at both the beginning
    (last.next) and the end (new node becomes last).

Time Complexity:
    - Insert at beginning: O(1) (with tail/last pointer)
    - Insert at end:       O(1) (with tail/last pointer)
    - Delete:              O(n)
    - Traversal:           O(n)
"""

from typing import Any, List, Optional, Tuple


class CNode:
    def __init__(self, data: Any):
        self.data: Any = data
        self.next: Optional["CNode"] = None

    def __repr__(self):
        return f"CNode({self.data})"


class CircularSinglyLinkedList:
    """
    Circular Singly Linked List maintained with a 'last' pointer.
    """
    def __init__(self):
        self.last: Optional[CNode] = None

    def is_empty(self) -> bool:
        return self.last is None

    def insert_at_beginning(self, data: Any) -> None:
        """Inserts a new node at the front. O(1)"""
        new_node = CNode(data)
        if self.is_empty():
            self.last = new_node
            self.last.next = self.last
        else:
            new_node.next = self.last.next
            self.last.next = new_node

    def insert_at_end(self, data: Any) -> None:
        """Inserts a new node at the end. O(1)"""
        new_node = CNode(data)
        if self.is_empty():
            self.last = new_node
            self.last.next = self.last
        else:
            new_node.next = self.last.next
            self.last.next = new_node
            self.last = new_node

    def delete_by_value(self, key: Any) -> bool:
        """Deletes a node containing key. Returns True if deleted."""
        if self.is_empty():
            return False

        curr = self.last.next
        prev = self.last

        # Search for key
        while True:
            if curr.data == key:
                if curr == self.last and curr.next == self.last:
                    # Only one node in list
                    self.last = None
                else:
                    prev.next = curr.next
                    if curr == self.last:
                        self.last = prev
                return True

            prev = curr
            curr = curr.next
            if curr == self.last.next:
                break

        return False

    def display(self) -> None:
        """Prints all elements in circular sequence."""
        if self.is_empty():
            print("Circular List is EMPTY.")
            return

        nodes = []
        curr = self.last.next
        while True:
            nodes.append(f"[{curr.data}]")
            curr = curr.next
            if curr == self.last.next:
                break

        print(" -> ".join(nodes) + f" -> (back to {self.last.next.data})")


def split_circular_list(clist: CircularSinglyLinkedList) -> Tuple[CircularSinglyLinkedList, CircularSinglyLinkedList]:
    """
    Splits a circular linked list into two equal (or balanced) circular linked lists.
    Uses Floyd's slow and fast pointer approach.
    """
    if clist.is_empty() or clist.last.next == clist.last:
        return clist, CircularSinglyLinkedList()

    head = clist.last.next
    slow = head
    fast = head

    # Fast moves 2 steps, slow moves 1 step
    while fast.next != head and fast.next.next != head:
        fast = fast.next.next
        slow = slow.next

    # If even number of elements, move fast to last node
    if fast.next.next == head:
        fast = fast.next

    # First half
    head1 = head
    last1 = slow

    # Second half
    head2 = slow.next
    last2 = fast

    # Make both halves circular
    last1.next = head1
    last2.next = head2

    list1 = CircularSinglyLinkedList()
    list1.last = last1

    list2 = CircularSinglyLinkedList()
    list2.last = last2

    return list1, list2


if __name__ == "__main__":
    print("=" * 65)
    print("     COLLEGE DSA LAB: CIRCULAR SINGLY LINKED LIST")
    print("=" * 65)

    clist = CircularSinglyLinkedList()
    for val in [10, 20, 30, 40, 50, 60]:
        clist.insert_at_end(val)

    print("Original Circular List:")
    clist.display()

    print("\nInserting 5 at beginning:")
    clist.insert_at_beginning(5)
    clist.display()

    print("\nDeleting 30:")
    clist.delete_by_value(30)
    clist.display()

    print("\nSplitting into two circular halves:")
    h1, h2 = split_circular_list(clist)
    print("Half 1: ", end="")
    h1.display()
    print("Half 2: ", end="")
    h2.display()
