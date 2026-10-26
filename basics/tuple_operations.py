"""
Tuple Operations and Immutability in Python
==========================================

This module demonstrates the semantics, features, and advantages of tuples in Python,
including immutability, sequence operations, unpacking, hashability, and NamedTuples.

Key Concepts Covered:
---------------------
1. Tuple instantiation, single-element syntax gotcha, and packing
2. Immutability guarantees and memory footprint comparison
3. Indexing and slice extraction
4. Methods: count() and index()
5. Unpacking patterns (multiple assignment, swap, starred unpacking)
6. Hashability: using tuples as dictionary keys and set elements
7. Structured records using typing.NamedTuple
"""

import sys
from typing import Any, Dict, List, NamedTuple, Tuple


class GeoCoordinate(NamedTuple):
    """Structured, immutable geographic coordinate with type hints."""
    latitude: float
    longitude: float
    city_name: str


def demonstrate_creation_and_gotchas() -> None:
    """
    Demonstrate tuple declaration and the single-element tuple comma rule.
    """
    print("=" * 60)
    print("1. TUPLE CREATION AND SYNTAX")
    print("=" * 60)

    standard_tuple: Tuple[int, ...] = (10, 20, 30, 40, 50)
    print(f"  Standard Tuple:                 {standard_tuple} (Type: {type(standard_tuple).__name__})")

    # The Single-element Gotcha: (42) is an int; (42,) is a tuple
    not_a_tuple = (42)
    valid_single_tuple: Tuple[int] = (42,)
    print(f"  Parentheses without comma (42): {not_a_tuple} (Type: {type(not_a_tuple).__name__})")
    print(f"  Parentheses with comma (42,):   {valid_single_tuple} (Type: {type(valid_single_tuple).__name__})")

    # Implicit packing without parentheses
    packed_tuple = 1, "two", 3.0
    print(f"  Packed without parens:          {packed_tuple} (Type: {type(packed_tuple).__name__})")
    print()


def demonstrate_immutability_and_memory() -> None:
    """
    Demonstrate immutability constraints and compare memory overhead with lists.
    """
    print("=" * 60)
    print("2. IMMUTABILITY AND MEMORY EFFICIENCY")
    print("=" * 60)

    immutable_tuple: Tuple[int, int, int] = (1, 2, 3)
    equivalent_list: List[int] = [1, 2, 3]

    print(f"  Tuple bytes in memory: {sys.getsizeof(immutable_tuple)} bytes")
    print(f"  List bytes in memory:  {sys.getsizeof(equivalent_list)} bytes")

    # Demonstrating immutability defense
    try:
        # Tuples do not support item assignment
        # Using Any to bypass static type-checker for demonstration
        untyped_tuple: Any = immutable_tuple
        untyped_tuple[0] = 99
    except TypeError as exc:
        print(f"  Immutability enforcement: Caught expected TypeError -> '{exc}'")

    # Caveat: Tuples can hold mutable objects (e.g. list inside tuple)
    hybrid_tuple: Tuple[Any, ...] = ([1, 2], "constant")
    hybrid_tuple[0].append(3)
    print(f"  Tuple containing mutable inner list: {hybrid_tuple}")
    print()


def demonstrate_slicing_and_methods() -> None:
    """
    Demonstrate indexing, slicing, and available tuple methods (count, index).
    """
    print("=" * 60)
    print("3. SLICING AND QUERY METHODS")
    print("=" * 60)

    sequence: Tuple[int, ...] = (2, 4, 5, 6, 7, 2, 8, 2)
    print(f"  Source Tuple:                  {sequence}")

    # Slicing
    slice_1: Tuple[int, ...] = sequence[1:4]
    prefix_slice: Tuple[int, ...] = sequence[:5]
    print(f"  Slice [1:4]:                   {slice_1}")
    print(f"  Prefix slice [:5]:             {prefix_slice}")

    # Built-in methods: count and index
    count_of_twos: int = sequence.count(2)
    first_index_of_seven: int = sequence.index(7)
    print(f"  Occurrences of value 2:        {count_of_twos}")
    print(f"  First index of value 7:        {first_index_of_seven}")
    print()


def demonstrate_unpacking_idioms() -> None:
    """
    Demonstrate tuple unpacking, variable swapping, and starred unpacking (*rest).
    """
    print("=" * 60)
    print("4. UNPACKING IDIOMS")
    print("=" * 60)

    # Standard unpacking
    point: Tuple[int, int, int] = (1920, 1080, 60)
    width, height, refresh_rate = point
    print(f"  Unpacked: Width={width}, Height={height}, Refresh={refresh_rate}Hz")

    # In-place variable swap without temporary variable
    x, y = 10, 20
    print(f"  Before swap: x={x}, y={y}")
    x, y = y, x
    print(f"  After swap:  x={x}, y={y}")

    # Extended (starred) unpacking (PEP 3132)
    milestones: Tuple[int, ...] = (2018, 2019, 2020, 2021, 2022, 2023, 2024)
    first_year, *middle_years, latest_year = milestones
    print(f"  First Year:   {first_year}")
    print(f"  Middle Years: {middle_years}")
    print(f"  Latest Year:  {latest_year}")
    print()


def demonstrate_hashability_and_namedtuples() -> None:
    """
    Demonstrate using tuples as dictionary keys and show modern typing.NamedTuple.
    """
    print("=" * 60)
    print("5. HASHABILITY AND NAMEDTUPLES")
    print("=" * 60)

    # Tuples containing only immutable objects are hashable -> usable as dict keys
    grid_matrix: Dict[Tuple[int, int], str] = {
        (0, 0): "Start",
        (1, 2): "Checkpoint A",
        (4, 5): "Destination",
    }
    print(f"  Matrix lookup at (1, 2): {grid_matrix[(1, 2)]}")

    # NamedTuple demonstration
    headquarters = GeoCoordinate(latitude=37.7749, longitude=-122.4194, city_name="San Francisco")
    print("\n  typing.NamedTuple Example:")
    print(f"    Record:      {headquarters}")
    print(f"    City:        {headquarters.city_name}")
    print(f"    Coordinates: ({headquarters.latitude}, {headquarters.longitude})")
    print(f"    Accessible by index: {headquarters[0]}, {headquarters[1]}")
    print()


def main() -> None:
    """Entry point for running tuple operations showcase."""
    print("PYTHON TUPLE OPERATIONS & PATTERNS")
    print()

    demonstrate_creation_and_gotchas()
    demonstrate_immutability_and_memory()
    demonstrate_slicing_and_methods()
    demonstrate_unpacking_idioms()
    demonstrate_hashability_and_namedtuples()


if __name__ == "__main__":
    main()