"""
Variables and Data Types in Python
==================================

This module demonstrates Python's fundamental data types, dynamic typing system,
memory identity, variable assignment conventions, and type conversion.

Key Concepts Covered:
---------------------
1. Primitive Types: int, float, complex, bool, str, NoneType
2. Collection Types: list, tuple, set, dict
3. Dynamic Typing & Type Inspection: type(), isinstance()
4. Object Identity vs. Value Equality: id(), 'is' vs. '=='
5. Mutability vs. Immutability
6. Explicit Type Casting & Truthiness Evaluation
7. PEP 8 Variable Naming Conventions
"""

from typing import Any, Dict, List, Set, Tuple


# PEP 8 Constant Convention: UPPER_CASE_WITH_UNDERSCORES
APPLICATION_NAME: str = "Python Fundamentals"
MAX_RETRY_COUNT: int = 3
PI_APPROXIMATION: float = 3.141592653589793


def demonstrate_primitive_types() -> Dict[str, Any]:
    """
    Demonstrate Python's standard built-in scalar/primitive data types.

    Returns:
        Dict[str, Any]: A dictionary mapping type names to sample values.
    """
    integer_val: int = 42
    float_val: float = 3.14159
    complex_val: complex = 2 + 3j
    boolean_val: bool = True
    string_val: str = "Hello, Python!"
    none_val: None = None

    samples: Dict[str, Any] = {
        "int": integer_val,
        "float": float_val,
        "complex": complex_val,
        "bool": boolean_val,
        "str": string_val,
        "NoneType": none_val,
    }

    print("=" * 60)
    print("1. PRIMITIVE DATA TYPES")
    print("=" * 60)
    for type_name, value in samples.items():
        print(f"  {type_name:<10} | Value: {repr(value):<20} | Type: {type(value).__name__}")
    print()

    return samples


def demonstrate_collection_types() -> None:
    """
    Demonstrate Python's primary built-in collection and container types.
    """
    sample_list: List[Any] = [1, 2, "apple", 4.5]
    sample_tuple: Tuple[int, str, float] = (10, "constant", 99.9)
    sample_set: Set[int] = {1, 2, 3, 3, 2, 1}  # Automatically deduplicated
    sample_dict: Dict[str, str] = {"name": "Alice", "role": "Engineer"}

    print("=" * 60)
    print("2. BUILT-IN COLLECTION TYPES")
    print("=" * 60)
    print(f"  List (mutable, ordered):        {sample_list}")
    print(f"  Tuple (immutable, ordered):     {sample_tuple}")
    print(f"  Set (mutable, unique items):    {sample_set}")
    print(f"  Dict (mutable, key-value pairs): {sample_dict}")
    print()


def demonstrate_identity_and_mutability() -> None:
    """
    Demonstrate the difference between value equality ('==') and object identity ('is'),
    along with mutability implications in memory.
    """
    print("=" * 60)
    print("3. OBJECT IDENTITY & MUTABILITY")
    print("=" * 60)

    # Immutability: Reassigning an integer or string creates a new object
    count_a: int = 1000
    count_b: int = 1000
    print(f"  count_a == count_b (Value match):    {count_a == count_b}")
    print(f"  count_a is count_b (Identity match): {count_a is count_b}")
    print(f"  id(count_a): {id(count_a)}, id(count_b): {id(count_b)}")

    # Mutability: Lists can be modified in-place without changing object ID
    original_list: List[int] = [1, 2, 3]
    initial_id: int = id(original_list)
    original_list.append(4)
    updated_id: int = id(original_list)

    print(f"  List before & after append has same ID: {initial_id == updated_id}")
    print(f"  Original list after mutation: {original_list}")

    # Aliasing vs. Copying
    alias_list: List[int] = original_list  # References same object in memory
    copy_list: List[int] = original_list.copy()  # Creates a distinct new object

    alias_list.append(5)
    print(f"  After mutating alias -> original_list: {original_list}")
    print(f"  After mutating alias -> copy_list:     {copy_list}")
    print()


def demonstrate_type_conversions() -> None:
    """
    Demonstrate explicit type casting and Python truthiness evaluations.
    """
    print("=" * 60)
    print("4. TYPE CASTING & TRUTH VALUE TESTING (TRUTHINESS)")
    print("=" * 60)

    # Type casting
    numeric_str: str = "128"
    converted_int: int = int(numeric_str)
    converted_float: float = float(numeric_str)
    print(f"  str '{numeric_str}' -> int: {converted_int} ({type(converted_int).__name__})")
    print(f"  str '{numeric_str}' -> float: {converted_float} ({type(converted_float).__name__})")

    # Sequence conversion
    tuple_source: Tuple[int, ...] = (1, 2, 3)
    list_result: List[int] = list(tuple_source)
    print(f"  tuple {tuple_source} -> list: {list_result}")

    # Truthiness: In Python, empty containers, 0, None, and False are Falsy
    falsy_values: List[Any] = [0, 0.0, "", [], (), {}, set(), None, False]
    print("\n  Falsy Values in Python (all evaluate to False):")
    for item in falsy_values:
        print(f"    bool({repr(item):<10}) -> {bool(item)}")

    truthy_values: List[Any] = [1, -5, "text", [0], {"key": False}]
    print("\n  Truthy Values (evaluate to True):")
    for item in truthy_values:
        print(f"    bool({repr(item):<12}) -> {bool(item)}")
    print()


def main() -> None:
    """Entry point for demonstrating variable and type handling."""
    print("PYTHON VARIABLES & DATA TYPES WORKSHOP")
    print("Application:", APPLICATION_NAME)
    print()

    demonstrate_primitive_types()
    demonstrate_collection_types()
    demonstrate_identity_and_mutability()
    demonstrate_type_conversions()


if __name__ == "__main__":
    main()