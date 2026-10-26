"""
Mathematical Operations and Standard Library Math Module
========================================================

This module demonstrates numerical computation, number theory, trigonometry,
floating-point precision handling, and constants available in Python's standard
'math' library.

Key Concepts Covered:
---------------------
1. Number Theory: gcd, lcm, factorial, permutations, combinations, isqrt
2. Power & Logarithms: pow, sqrt, exp, log, log2, log10
3. Trigonometry & Angular Conversions: sin, cos, tan, hypot, radians, degrees
4. Precision & Rounding: ceil, floor, trunc, fabs, fmod, remainder, isclose
5. Aggregations & Constants: prod, pi, e, tau, inf, nan
"""

import math
from typing import List, Tuple


def demonstrate_number_theory() -> None:
    """
    Demonstrate integer and discrete mathematics functions.
    """
    print("=" * 60)
    print("1. NUMBER THEORY AND INTEGER ARITHMETIC")
    print("=" * 60)

    a, b = 12, 18
    gcd_val = math.gcd(a, b)
    lcm_val = math.lcm(a, b)
    print(f"  Greatest Common Divisor: gcd({a}, {b}) = {gcd_val}")
    print(f"  Least Common Multiple:   lcm({a}, {b}) = {lcm_val}")

    n = 5
    fact_n = math.factorial(n)
    print(f"  Factorial:               factorial({n}) = {fact_n}")

    # Combinatorics (Python 3.8+)
    n_items, k_items = 5, 2
    comb_val = math.comb(n_items, k_items)
    perm_val = math.perm(n_items, k_items)
    print(f"  Combinations:            comb({n_items}, {k_items}) = {comb_val}")
    print(f"  Permutations:            perm({n_items}, {k_items}) = {perm_val}")

    # Exact integer square root
    perfect_sq, non_perfect = 25, 27
    print(f"  Integer Square Root:     isqrt({perfect_sq}) = {math.isqrt(perfect_sq)}")
    print(f"  Integer Square Root:     isqrt({non_perfect}) = {math.isqrt(non_perfect)}")
    print()


def demonstrate_powers_and_logarithms() -> None:
    """
    Demonstrate power, exponential, and logarithmic functions.
    """
    print("=" * 60)
    print("2. EXPONENTIAL AND LOGARITHMIC FUNCTIONS")
    print("=" * 60)

    val = 16.0
    print(f"  Square Root:             sqrt({val}) = {math.sqrt(val)}")
    print(f"  Power:                   pow(2, 3) = {math.pow(2, 3)}")
    print(f"  Exponential:             exp(2) = e^2 ~= {math.exp(2):.6f}")

    # Logarithms
    print(f"  Natural Log:             log(e) = {math.log(math.e)}")
    print(f"  Base-10 Log:             log(100, 10) = {math.log(100, 10)}")
    print(f"  Optimized Base-10:       log10(100) = {math.log10(100)}")
    print(f"  Optimized Base-2:        log2(32) = {math.log2(32)}")
    print()


def demonstrate_trigonometry() -> None:
    """
    Demonstrate trigonometric functions and degree/radian angular conversions.
    """
    print("=" * 60)
    print("3. TRIGONOMETRY AND ANGULAR CONVERSIONS")
    print("=" * 60)

    # Note: Python math trig functions expect angles in radians
    angle_deg = 180.0
    angle_rad = math.radians(angle_deg)
    back_to_deg = math.degrees(angle_rad)
    print(f"  Degrees to Radians:      radians({angle_deg} deg) = {angle_rad:.6f} rad (pi)")
    print(f"  Radians to Degrees:      degrees(pi) = {back_to_deg:.1f} deg")

    # Sine and Cosine
    sin_pi_over_2 = math.sin(math.pi / 2)
    cos_zero = math.cos(0)
    sin_zero = math.sin(0)
    cos_deg_90_in_rad = math.cos(math.radians(90))  # Note: math.cos(90) treats 90 as radians!
    print(f"  sin(pi / 2):             {sin_pi_over_2}")
    print(f"  cos(0):                  {cos_zero}")
    print(f"  sin(0):                  {sin_zero}")
    print(f"  cos(90 deg in radians):  {cos_deg_90_in_rad:.6e} (~= 0)")

    # Euclidean distance (hypotenuse)
    x, y = 3.0, 4.0
    hypot_val = math.hypot(x, y)
    print(f"  Hypotenuse:              hypot({x}, {y}) = {hypot_val}")
    print()


def demonstrate_rounding_and_precision() -> None:
    """
    Demonstrate rounding, modulo operations, and IEEE 754 floating-point comparison.
    """
    print("=" * 60)
    print("4. ROUNDING, FLOATS, AND PRECISION COMPARISON")
    print("=" * 60)

    num_a, num_b = 4.2, 4.8
    print(f"  Ceiling:                 ceil({num_a}) = {math.ceil(num_a)}")
    print(f"  Floor:                   floor({num_b}) = {math.floor(num_b)}")
    print(f"  Truncation:              trunc(-4.9) = {math.trunc(-4.9)}")
    print(f"  Absolute Float Value:    fabs(-5.5) = {math.fabs(-5.5)}")

    # Floating point remainders: fmod vs. remainder
    print(f"  fmod(10, 3):             {math.fmod(10, 3)} (sign of dividend)")
    print(f"  remainder(10, 3):        {math.remainder(10, 3)} (IEEE 754 rounded remainder)")

    # The famous floating point equality pitfall: 0.1 + 0.2 != 0.3
    direct_eq = (0.1 + 0.2) == 0.3
    isclose_eq = math.isclose(0.1 + 0.2, 0.3)
    print(f"\n  Floating point comparison (0.1 + 0.2 == 0.3):")
    print(f"    Direct equality (==):   {direct_eq} (Raw sum: {0.1 + 0.2})")
    print(f"    math.isclose():         {isclose_eq} (Correct professional practice)")
    print()


def demonstrate_aggregations_and_constants() -> None:
    """
    Demonstrate product aggregation and mathematical constants.
    """
    print("=" * 60)
    print("5. AGGREGATIONS AND CONSTANTS")
    print("=" * 60)

    factors: List[int] = [1, 2, 3, 4]
    product_val = math.prod(factors)
    print(f"  Product of {factors}: math.prod(...) = {product_val}")

    print("\n  Fundamental Mathematical Constants:")
    print(f"    pi      = {math.pi}")
    print(f"    e       = {math.e}")
    print(f"    tau     = {math.tau} (2 * pi)")
    print(f"    inf     = {math.inf} (isinf: {math.isinf(math.inf)})")
    print(f"    nan     = {math.nan} (isnan: {math.isnan(math.nan)})")
    print()


def main() -> None:
    """Entry point for executing math module demonstrations."""
    print("PYTHON STANDARD LIBRARY MATH OPERATIONS")
    print()

    demonstrate_number_theory()
    demonstrate_powers_and_logarithms()
    demonstrate_trigonometry()
    demonstrate_rounding_and_precision()
    demonstrate_aggregations_and_constants()


if __name__ == "__main__":
    main()