"""
List Operations and Sequences in Python
=======================================

This module demonstrates idiomatic and efficient operations on Python lists,
covering indexing, slicing, in-place mutations, sorting, searching, copying,
and list comprehensions.

Key Concepts Covered:
---------------------
1. List instantiation, indexing, and boundary handling
2. Slice notation: [start:stop:step] and reverse slicing [::-1]
3. Mutation methods: append, extend, insert, pop, remove, clear
4. Query methods: count, index, membership testing ('in')
5. In-place sorting (list.sort) vs. functional sorting (sorted())
6. Shallow copies vs. deep copies (copy module)
7. List comprehensions for functional mapping and filtering
8. Iteration idioms: enumerate() and zip()
"""

import copy
from typing import Any, List, Optional, Tuple


def demonstrate_indexing_and_slicing() -> None:
    """
    Demonstrate forward and negative indexing alongside comprehensive slice notations.
    """
    print("=" * 60)
    print("1. INDEXING AND SLICING")
    print("=" * 60)

    data: List[int] = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    print(f"  Source List: {data} (Length: {len(data)})")

    # Single element indexing
    first_elem: int = data[0]
    last_elem: int = data[-1]
    second_last: int = data[-2]
    print(f"  First element (data[0]):       {first_elem}")
    print(f"  Last element (data[-1]):       {last_elem}")
    print(f"  Second last (data[-2]):        {second_last}")

    # Slicing: [start:stop] (stop is non-inclusive)
    sub_slice_1: List[int] = data[1:4]   # Elements from index 1 up to (not including) 4
    sub_slice_2: List[int] = data[:3]    # Elements from start up to index 3
    sub_slice_3: List[int] = data[6:]    # Elements from index 6 to the end
    print(f"  Slice [1:4]:                   {sub_slice_1}")
    print(f"  Prefix slice [:3]:             {sub_slice_2}")
    print(f"  Suffix slice [6:]:             {sub_slice_3}")

    # Strided Slicing: [start:stop:step]
    every_second: List[int] = data[::2]
    reversed_list: List[int] = data[::-1]
    print(f"  Strided slice [::2]:           {every_second}")
    print(f"  Reversed slice [::-1]:         {reversed_list}")
    print()


def demonstrate_mutation_methods() -> None:
    """
    Demonstrate in-place modifications using standard list methods.
    """
    print("=" * 60)
    print("2. IN-PLACE LIST MUTATIONS")
    print("=" * 60)

    items: List[str] = ["alpha", "beta", "gamma"]
    print(f"  Initial list:                  {items}")

    # Append: Adds a single element to the end
    items.append("delta")
    print(f"  After append('delta'):         {items}")

    # Extend: Appends all items from an iterable
    items.extend(["epsilon", "zeta"])
    print(f"  After extend(['epsilon', 'zeta']): {items}")

    # Insert: Inserts an element at a specified index
    items.insert(2, "beta_prime")
    print(f"  After insert(2, 'beta_prime'): {items}")

    # Remove: Removes first occurrence of a value
    items.remove("beta_prime")
    print(f"  After remove('beta_prime'):    {items}")

    # Pop: Removes and returns element at given index (defaults to -1)
    popped_item: str = items.pop()
    print(f"  Popped item from tail:         '{popped_item}'")
    print(f"  List after pop():              {items}")

    popped_indexed: str = items.pop(0)
    print(f"  Popped item from index 0:      '{popped_indexed}'")
    print(f"  List after pop(0):             {items}")
    print()


def demonstrate_searching_and_sorting() -> None:
    """
    Demonstrate membership testing, frequency counting, and custom sorting.
    """
    print("=" * 60)
    print("3. SEARCHING AND SORTING")
    print("=" * 60)

    scores: List[int] = [75, 92, 88, 75, 100, 64, 75, 92]
    print(f"  Scores:                        {scores}")

    # Membership and counting
    target: int = 75
    exists: bool = target in scores
    count_75: int = scores.count(target)
    first_idx: int = scores.index(target)
    print(f"  Is {target} in scores?:            {exists}")
    print(f"  Frequency of {target}:             {count_75}")
    print(f"  First index of {target}:           {first_idx}")

    # Functional sorting with sorted() (does not mutate original)
    sorted_asc: List[int] = sorted(scores)
    sorted_desc: List[int] = sorted(scores, reverse=True)
    print(f"  Functional sorted() (asc):     {sorted_asc}")
    print(f"  Functional sorted() (desc):    {sorted_desc}")
    print(f"  Original remains unmodified:   {scores}")

    # In-place sorting with .sort()
    words: List[str] = ["banana", "pie", "apple", "elderberry", "cherry"]
    # Sort in-place by word length, then alphabetically
    words.sort(key=lambda w: (len(w), w))
    print(f"  Words sorted by length, then alphabet: {words}")
    print()


def demonstrate_copying() -> None:
    """
    Demonstrate shallow copy vs. deep copy when dealing with nested structures.
    """
    print("=" * 60)
    print("4. REFERENCE VS. SHALLOW COPY VS. DEEP COPY")
    print("=" * 60)

    nested_original: List[List[int]] = [[1, 2], [3, 4]]
    shallow_copy: List[List[int]] = nested_original.copy()
    deep_copied: List[List[int]] = copy.deepcopy(nested_original)

    # Modifying an inner mutable element
    nested_original[0].append(99)

    print(f"  Original after mutating sublist: {nested_original}")
    print(f"  Shallow Copy (affected!):        {shallow_copy}")
    print(f"  Deep Copy (unaffected!):         {deep_copied}")
    print()


def demonstrate_comprehensions_and_utilities() -> None:
    """
    Demonstrate idiomatic list comprehensions, enumerate, and zip.
    """
    print("=" * 60)
    print("5. LIST COMPREHENSIONS AND ITERATION IDIOMS")
    print("=" * 60)

    numbers: List[int] = list(range(1, 11))

    # Filtering and mapping in a single comprehension
    even_squares: List[int] = [x ** 2 for x in numbers if x % 2 == 0]
    print(f"  Even squares (1..10):          {even_squares}")

    # Conditional transformation (ternary expression inside comprehension)
    labels: List[str] = ["EVEN" if x % 2 == 0 else "ODD" for x in numbers[:6]]
    print(f"  Parity labels:                 {labels}")

    # Enumerate demonstration
    fruits: List[str] = ["Apple", "Mango", "Blueberry"]
    print("\n  Indexed iteration with enumerate():")
    for idx, fruit in enumerate(fruits, start=1):
        print(f"    Item #{idx}: {fruit}")

    # Zip demonstration
    quantities: List[int] = [10, 5, 25]
    print("\n  Parallel iteration with zip():")
    for fruit, qty in zip(fruits, quantities):
        print(f"    {fruit:<10} -> Stock: {qty} units")
    print()


def main() -> None:
    """Entry point for demonstrating Python list functionality."""
    print("PYTHON LIST OPERATIONS & SEQUENCE PROCESSING")
    print()

    demonstrate_indexing_and_slicing()
    demonstrate_mutation_methods()
    demonstrate_searching_and_sorting()
    demonstrate_copying()
    demonstrate_comprehensions_and_utilities()


if __name__ == "__main__":
    main()