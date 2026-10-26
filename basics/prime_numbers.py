"""
Prime Number Algorithms and Utilities in Python
===============================================

This module provides high-performance, mathematically rigorous utilities for
primality testing, prime sequence generation, and prime factorization.

Key Concepts Covered:
---------------------
1. Primality testing with 6k ± 1 trial division optimization (O(sqrt(n)))
2. Sieve of Eratosthenes for bulk prime generation (O(n log log n))
3. Stream generation of the first N prime numbers
4. Prime factorization (Fundamental Theorem of Arithmetic)
5. Comprehensive input validation and type annotations
"""

import math
from typing import Generator, List, Tuple


def is_prime(n: int) -> bool:
    """
    Determine whether an integer is prime using 6k ± 1 trial division.

    Complexity:
        Time:  O(sqrt(n)) in the worst case (pruned quickly for composites)
        Space: O(1)

    Args:
        n: Integer to test for primality.

    Returns:
        True if n is prime; False otherwise (including negatives, 0, and 1).
    """
    if n <= 1:
        return False
    if n <= 3:
        return True  # 2 and 3 are prime
    if n % 2 == 0 or n % 3 == 0:
        return False

    # All primes greater than 3 can be expressed in the form 6k ± 1
    # Check factors up to floor(sqrt(n)) with stride 6
    limit = math.isqrt(n)
    for i in range(5, limit + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False

    return True


def sieve_of_eratosthenes(limit: int) -> List[int]:
    """
    Generate all prime numbers up to a specified inclusive upper bound
    using the classical Sieve of Eratosthenes algorithm.

    Complexity:
        Time:  O(n log log n)
        Space: O(n) using a compact bytearray

    Args:
        limit: Upper inclusive bound for primes.

    Returns:
        Ascending list of all prime numbers <= limit.
    """
    if limit < 2:
        return []

    # Use bytearray for cache locality and minimal memory overhead
    is_prime_sieve = bytearray([1]) * (limit + 1)
    is_prime_sieve[0] = 0
    is_prime_sieve[1] = 0

    upper_check = math.isqrt(limit)
    for p in range(2, upper_check + 1):
        if is_prime_sieve[p]:
            # Mark multiples starting from p * p
            is_prime_sieve[p * p : limit + 1 : p] = bytearray(len(range(p * p, limit + 1, p)))

    return [num for num, active in enumerate(is_prime_sieve) if active]


def first_n_primes(count: int) -> List[int]:
    """
    Generate a list containing the first N prime numbers.

    Args:
        count: Desired number of primes to generate (must be non-negative).

    Returns:
        List containing the first 'count' prime numbers.

    Raises:
        ValueError: If count is negative.
    """
    if count < 0:
        raise ValueError("Prime count cannot be negative.")
    if count == 0:
        return []

    primes: List[int] = [2]
    candidate = 3

    while len(primes) < count:
        if is_prime(candidate):
            primes.append(candidate)
        candidate += 2  # Skip even candidates

    return primes


def prime_factors(n: int) -> List[int]:
    """
    Compute the complete prime factorization of an integer n.

    Args:
        n: Integer to factorize (must be >= 2).

    Returns:
        List of prime factors whose product equals n.

    Raises:
        ValueError: If n < 2.
    """
    if n < 2:
        raise ValueError("Factorization requires an integer >= 2.")

    factors: List[int] = []

    # Factor out twos
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    # Factor out odd components up to sqrt(n)
    divisor = 3
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        divisor += 2

    if n > 1:
        factors.append(n)

    return factors


def main() -> None:
    """Demonstrate prime number operations and verification tests."""
    print("=" * 60)
    print("PRIME NUMBER ALGORITHMS & NUMBER THEORY")
    print("=" * 60)

    # 1. First N Primes
    n_count = 10
    primes_10 = first_n_primes(n_count)
    print(f"1. First {n_count} Primes:")
    print(f"   {primes_10}\n")

    # 2. Primality Testing with 6k ± 1 Optimization
    test_values = [-7, 0, 1, 2, 17, 27, 97, 100, 1009, 1013]
    print("2. Primality Test Matrix:")
    for val in test_values:
        status = "PRIME" if is_prime(val) else "COMPOSITE / NON-PRIME"
        print(f"   Value {val:>5}: {status}")
    print()

    # 3. Sieve of Eratosthenes (Primes up to limit)
    limit = 50
    sieved_primes = sieve_of_eratosthenes(limit)
    print(f"3. Sieve of Eratosthenes (Primes <= {limit}):")
    print(f"   {sieved_primes}")
    print(f"   Total primes found: {len(sieved_primes)}\n")

    # 4. Prime Factorization
    numbers_to_factor = [24, 84, 315, 1024, 1009]
    print("4. Prime Factorization:")
    for num in numbers_to_factor:
        factors = prime_factors(num)
        factor_str = " * ".join(map(str, factors))
        print(f"   {num:>4} = {factor_str}")
    print()


if __name__ == "__main__":
    main()
