"""
Random Number Generation and Sampling in Python
===============================================

This module demonstrates pseudo-random number generation (PRNG) using Python's
built-in 'random' module, covering scalar generation, sequence manipulation,
weighted selections, distributions, and cryptographic security considerations.

Key Concepts Covered:
---------------------
1. Scalar generation: random(), uniform(), randint(), randrange()
2. Sequence operations: choice(), choices() (with replacement & weights), sample() (without replacement)
3. In-place sequence mutation: shuffle()
4. Reproducibility via pseudo-random state seeding: seed()
5. Continuous probability distributions: gauss(), triangular()
6. Security notice: PRNG (random) vs. Cryptographically Secure PRNG (secrets)
"""

import random
import secrets
from typing import Any, List, Sequence, TypeVar

T = TypeVar("T")


def demonstrate_scalar_generation() -> None:
    """
    Demonstrate generating random floats and integers across various intervals.
    """
    print("=" * 60)
    print("1. SCALAR RANDOM NUMBER GENERATION")
    print("=" * 60)

    # Unit interval float [0.0, 1.0)
    rand_float_1 = random.random()
    rand_float_2 = random.random()
    print(f"  Unit Float [0.0, 1.0):       {rand_float_1:.6f}")
    print(f"  Unit Float [0.0, 1.0):       {rand_float_2:.6f}")

    # Bounded float [a, b]
    bounded_float = random.uniform(10.5, 25.0)
    print(f"  Uniform Float [10.5, 25.0]:  {bounded_float:.4f}")

    # Inclusive random integer [a, b]
    rand_int = random.randint(3, 9)
    print(f"  Random Integer [3, 9]:       {rand_int}")

    # Stepped integer from range(start, stop, step)
    rand_stepped = random.randrange(10, 100, 5)
    print(f"  Randrange (step of 5):       {rand_stepped}")
    print()


def demonstrate_sequence_sampling() -> None:
    """
    Demonstrate picking single elements, weighted choices with replacement,
    sampling without replacement, and in-place shuffling.
    """
    print("=" * 60)
    print("2. SEQUENCE SAMPLING AND SHUFFLING")
    print("=" * 60)

    deck: List[str] = ["Ace", "King", "Queen", "Jack", "10", "9"]
    print(f"  Original Deck:               {deck}")

    # Single random pick
    picked_card = random.choice(deck)
    print(f"  random.choice() single pick: '{picked_card}'")

    # Sample without replacement (unique elements)
    hand = random.sample(deck, k=3)
    print(f"  random.sample() unique 3:    {hand}")

    # In-place Fisher-Yates shuffle
    mutable_deck = deck.copy()
    random.shuffle(mutable_deck)
    print(f"  random.shuffle() in-place:   {mutable_deck}")

    # Weighted choices with replacement (k samples)
    categories = ["Bronze", "Silver", "Gold", "Platinum"]
    weights = [70, 20, 8, 2]  # Heavily weighted toward Bronze
    sampled_rewards = random.choices(categories, weights=weights, k=10)
    print(f"\n  Weighted random.choices() (k=10, 70% Bronze bias):")
    print(f"    {sampled_rewards}")
    print()


def demonstrate_reproducibility() -> None:
    """
    Demonstrate how seeding the Mersenne Twister engine produces deterministic sequences.
    """
    print("=" * 60)
    print("3. DETERMINISTIC SEEDING (REPRODUCIBILITY)")
    print("=" * 60)

    fixed_seed = 42

    random.seed(fixed_seed)
    run_a = [random.randint(1, 100) for _ in range(5)]

    random.seed(fixed_seed)
    run_b = [random.randint(1, 100) for _ in range(5)]

    print(f"  Seed {fixed_seed} Run A: {run_a}")
    print(f"  Seed {fixed_seed} Run B: {run_b}")
    print(f"  Identical sequence guaranteed: {run_a == run_b}")

    # Re-seed with system entropy to restore randomness
    random.seed(None)
    print()


def demonstrate_distributions() -> None:
    """
    Demonstrate non-uniform probability distributions (Gaussian / Normal).
    """
    print("=" * 60)
    print("4. PROBABILITY DISTRIBUTIONS")
    print("=" * 60)

    mean_value = 100.0
    std_deviation = 15.0
    iq_samples = [random.gauss(mean_value, std_deviation) for _ in range(5)]

    print(f"  Gaussian Samples (Mean={mean_value}, StDev={std_deviation}):")
    for idx, sample in enumerate(iq_samples, start=1):
        print(f"    Sample #{idx}: {sample:.2f}")
    print()


def demonstrate_cryptographic_security() -> None:
    """
    Demonstrate when and how to use Python's 'secrets' module instead of 'random'.
    """
    print("=" * 60)
    print("5. SECURITY: 'random' (PRNG) VS. 'secrets' (CSPRNG)")
    print("=" * 60)
    print("  [NOTE] The 'random' module is NOT cryptographically secure.")
    print("         Never use 'random' for security tokens, passwords, or authentication keys.")
    print("         Instead, use the standard library 'secrets' module:")

    secure_token_hex = secrets.token_hex(16)
    secure_url_token = secrets.token_urlsafe(16)
    secure_integer = secrets.randbelow(100)

    print(f"  CSPRNG Hex Token (32-char):   {secure_token_hex}")
    print(f"  CSPRNG URL-Safe Token:        {secure_url_token}")
    print(f"  CSPRNG Randbelow (0..99):     {secure_integer}")
    print()


def main() -> None:
    """Entry point for executing random module demonstrations."""
    print("PYTHON RANDOM & SAMPLING OPERATIONS WORKSHOP")
    print()

    demonstrate_scalar_generation()
    demonstrate_sequence_sampling()
    demonstrate_reproducibility()
    demonstrate_distributions()
    demonstrate_cryptographic_security()


if __name__ == "__main__":
    main()