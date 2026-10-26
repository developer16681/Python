"""
Experiment: Implement Two Stacks in a Single Array
---------------------------------------------------
Aim:
    To implement two stacks efficiently in a single one-dimensional array such
    that neither stack overflows unless the total combined number of elements
    equals the array's full capacity.

Theory:
    Instead of dividing the array strictly into two equal halves (which wastes
    space if one stack is full while the other is empty), start Stack 1 from
    the leftmost index (0) moving rightward, and start Stack 2 from the rightmost
    index (n - 1) moving leftward.
    
    - top1 starts at -1 and increments on push1.
    - top2 starts at n and decrements on push2.
    - An overflow occurs only when top1 + 1 == top2.

Time Complexity:
    - push1(), push2(): O(1)
    - pop1(), pop2():   O(1)

Space Complexity:
    - O(n) total fixed memory space.
"""

from typing import Any, List


class TwoStacks:
    """
    Two independent stacks sharing a single array from opposite ends.
    """
    def __init__(self, capacity: int = 10):
        if capacity < 2:
            raise ValueError("Capacity must be at least 2.")
        self.capacity = capacity
        self.arr: List[Any] = [None] * capacity
        self.top1 = -1
        self.top2 = capacity

    def push1(self, val: Any) -> None:
        """Pushes an element to Stack 1."""
        if self.top1 < self.top2 - 1:
            self.top1 += 1
            self.arr[self.top1] = val
        else:
            raise OverflowError("Stack Overflow! Both stacks have met.")

    def push2(self, val: Any) -> None:
        """Pushes an element to Stack 2."""
        if self.top1 < self.top2 - 1:
            self.top2 -= 1
            self.arr[self.top2] = val
        else:
            raise OverflowError("Stack Overflow! Both stacks have met.")

    def pop1(self) -> Any:
        """Pops an element from Stack 1."""
        if self.top1 >= 0:
            val = self.arr[self.top1]
            self.arr[self.top1] = None
            self.top1 -= 1
            return val
        raise IndexError("Stack Underflow in Stack 1.")

    def pop2(self) -> Any:
        """Pops an element from Stack 2."""
        if self.top2 < self.capacity:
            val = self.arr[self.top2]
            self.arr[self.top2] = None
            self.top2 += 1
            return val
        raise IndexError("Stack Underflow in Stack 2.")

    def display(self) -> None:
        """Shows memory layout of the shared array."""
        print(f"Memory Array Layout (Capacity={self.capacity}):")
        print(f"Array: {self.arr}")
        print(f"Stack 1 elements (top={self.top1}): {self.arr[:self.top1 + 1]}")
        print(f"Stack 2 elements (top={self.top2}): {self.arr[self.top2:]}\n")


if __name__ == "__main__":
    print("=" * 60)
    print("     COLLEGE DSA LAB: TWO STACKS IN A SINGLE ARRAY")
    print("=" * 60)

    ts = TwoStacks(capacity=6)

    # Push to Stack 1
    ts.push1(10)
    ts.push1(20)
    ts.push1(30)

    # Push to Stack 2
    ts.push2(99)
    ts.push2(88)

    ts.display()

    # Fill final slot using Stack 2
    ts.push2(77)
    ts.display()

    # Test overflow
    try:
        print("Attempting to push to Stack 1 when array is full:")
        ts.push1(40)
    except OverflowError as e:
        print(f"Caught: {e}")

    # Pop operations
    print(f"\nPopped from Stack 1: {ts.pop1()}")
    print(f"Popped from Stack 2: {ts.pop2()}")
    ts.display()
