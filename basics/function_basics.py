"""
Function Definitions and Arguments in Python
============================================

This module demonstrates professional function design in Python, adhering to
PEP 8 conventions, PEP 257 docstrings, and PEP 484 type hints.

Key Concepts Covered:
---------------------
1. Function definitions, docstrings, and explicit type annotations
2. Positional, default, and keyword arguments
3. Positional-only (/) and keyword-only (*) parameter syntax (PEP 570, PEP 3102)
4. Variadic arguments: *args and **kwargs
5. Multiple return values via tuple packing/unpacking
6. Pure functions vs. side-effects
7. Higher-order functions, closures, and lambdas
"""

from typing import Callable, Dict, List, Optional, Tuple, Union

Number = Union[int, float]


def add(a: Number, b: Number) -> Number:
    """
    Compute the arithmetic sum of two numbers.

    Args:
        a: First addend.
        b: Second addend.

    Returns:
        The sum of a and b.
    """
    return a + b


def subtract(a: Number, b: Number) -> Number:
    """
    Compute the difference between two numbers.

    Args:
        a: Minuend.
        b: Subtrahend.

    Returns:
        The difference resulting from subtracting b from a.
    """
    return a - b


def multiply(a: Number, b: Number) -> Number:
    """
    Compute the product of two numbers.

    Args:
        a: Multiplicand.
        b: Multiplier.

    Returns:
        The product of a and b.
    """
    return a * b


def divide(a: Number, b: Number) -> float:
    """
    Compute the quotient of two numbers with defensive zero-division check.

    Args:
        a: Dividend.
        b: Divisor.

    Returns:
        The float quotient of a divided by b.

    Raises:
        ZeroDivisionError: If b is zero.
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b


def calculate_statistics(numbers: List[Number]) -> Tuple[Number, Number, float]:
    """
    Calculate minimum, maximum, and average of a sequence.
    Demonstrates returning multiple values as a tuple.

    Args:
        numbers: Non-empty list of numeric values.

    Returns:
        Tuple containing (min_value, max_value, average).

    Raises:
        ValueError: If numbers list is empty.
    """
    if not numbers:
        raise ValueError("Cannot calculate statistics on an empty collection.")

    min_val = min(numbers)
    max_val = max(numbers)
    average = sum(numbers) / len(numbers)
    return min_val, max_val, average


def create_user_profile(
    user_id: int,
    username: str,
    /,  # Positional-only parameters before '/'
    email: str,
    role: str = "viewer",  # Default parameter
    *,  # Keyword-only parameters after '*'
    is_active: bool = True,
    metadata: Optional[Dict[str, str]] = None,
) -> Dict[str, Union[int, str, bool, Dict[str, str]]]:
    """
    Create a structured user dictionary demonstrating parameter categories:
    positional-only, standard positional/keyword, default, and keyword-only.

    Args:
        user_id: Unique integer identifier (positional-only).
        username: String handle (positional-only).
        email: Contact email address.
        role: Access level string (defaults to 'viewer').
        is_active: Account status flag (keyword-only).
        metadata: Optional dictionary of extra attributes (keyword-only).

    Returns:
        A dictionary containing the sanitized user profile.
    """
    profile: Dict[str, Union[int, str, bool, Dict[str, str]]] = {
        "user_id": user_id,
        "username": username,
        "email": email,
        "role": role,
        "is_active": is_active,
        "metadata": metadata if metadata is not None else {},
    }
    return profile


def sum_variadic(*values: Number, scale: float = 1.0) -> float:
    """
    Sum an arbitrary number of numeric arguments (*args) and multiply by a scale factor.

    Args:
        *values: Variable number of numeric values.
        scale: Factor to multiply the resulting sum.

    Returns:
        Scaled total.
    """
    return float(sum(values) * scale)


def configure_service(service_name: str, **settings: Union[str, int, bool]) -> None:
    """
    Configure a service using arbitrary keyword arguments (**kwargs).

    Args:
        service_name: Name of the target service.
        **settings: Key-value configuration pairs.
    """
    print(f"  Configuring [{service_name}]:")
    for key, val in sorted(settings.items()):
        print(f"    - {key}: {val}")


def apply_transformation(
    values: List[Number],
    transform: Callable[[Number], Number],
) -> List[Number]:
    """
    Demonstrate higher-order functions by accepting a callable argument.

    Args:
        values: List of numbers to transform.
        transform: A callable taking a number and returning a number.

    Returns:
        New list of transformed numbers.
    """
    return [transform(val) for val in values]


def make_multiplier(factor: Number) -> Callable[[Number], Number]:
    """
    Create a closure that multiplies its input by a pre-configured factor.

    Args:
        factor: Multiplier to encapsulate in the closure scope.

    Returns:
        A function that multiplies any number by factor.
    """
    def multiplier(x: Number) -> Number:
        return x * factor

    return multiplier


def main() -> None:
    """Demonstrate function calls, argument passing, and closures."""
    print("=" * 60)
    print("PYTHON FUNCTION ARCHITECTURE & CALL PATTERNS")
    print("=" * 60)

    # 1. Basic Arithmetic Operations (Pure Functions)
    print("1. Pure Arithmetic Functions:")
    print(f"  add(15, 27)       = {add(15, 27)}")
    print(f"  subtract(50, 18)  = {subtract(50, 18)}")
    print(f"  multiply(6, 7)    = {multiply(6, 7)}")
    print(f"  divide(100, 8)    = {divide(100, 8):.2f}\n")

    # 2. Multiple Return Values (Tuple Unpacking)
    print("2. Multiple Return Values:")
    data_points = [23, 88, 45, 92, 11, 67, 34]
    minimum, maximum, mean = calculate_statistics(data_points)
    print(f"  Dataset: {data_points}")
    print(f"  Min: {minimum} | Max: {maximum} | Mean: {mean:.2f}\n")

    # 3. Positional-only and Keyword-only Arguments
    print("3. Parameter Constraints (/, *):")
    user = create_user_profile(
        101,
        "alex_dev",
        email="alex@example.com",
        role="administrator",
        is_active=True,
        metadata={"region": "us-east-1", "tier": "gold"},
    )
    print(f"  User Profile: {user}\n")

    # 4. Variadic Arguments (*args and **kwargs)
    print("4. Variadic Arguments (*args, **kwargs):")
    total = sum_variadic(1, 2, 3, 4, 5, scale=2.5)
    print(f"  sum_variadic(1, 2, 3, 4, 5, scale=2.5) = {total}")
    configure_service("DatabasePool", host="localhost", port=5432, ssl=True, timeout=30)
    print()

    # 5. Higher-Order Functions & Closures
    print("5. Higher-Order Functions & Closures:")
    raw_nums: List[Number] = [1, 2, 3, 4, 5]
    doubled = apply_transformation(raw_nums, lambda x: x * 2)
    squared = apply_transformation(raw_nums, lambda x: x ** 2)
    print(f"  Original: {raw_nums}")
    print(f"  Doubled (Lambda): {doubled}")
    print(f"  Squared (Lambda): {squared}")

    triple = make_multiplier(3)
    print(f"  Closure make_multiplier(3)(10) = {triple(10)}")
    print()


if __name__ == "__main__":
    main()
