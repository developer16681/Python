"""
Time Operations and Performance Benchmarking in Python
======================================================

This module demonstrates timestamps, clock management, date/time string formatting,
and high-precision performance benchmarking using Python's standard 'time' module.

Key Concepts Covered:
---------------------
1. UNIX Epoch timestamps: time.time() and time.ctime()
2. Struct time representations: time.localtime() and time.gmtime() (UTC)
3. String formatting and parsing: strftime() and strptime()
4. High-resolution benchmarking: time.perf_counter() vs. time.process_time()
5. Monotonic clocks vs. wall clocks
6. Professional benchmarking tools: Timer context manager and decorator
"""

import functools
import time
from typing import Any, Callable, Optional


class BenchmarkTimer:
    """
    Context manager for high-precision block execution timing using time.perf_counter().
    """

    def __init__(self, description: str = "Execution"):
        self.description = description
        self.start_time: float = 0.0
        self.elapsed: float = 0.0

    def __enter__(self) -> "BenchmarkTimer":
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.elapsed = time.perf_counter() - self.start_time
        print(f"  [Timer] {self.description}: {self.elapsed * 1000:.3f} ms")


def benchmark(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator that logs the wall-clock execution time of a target function.
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"  [@benchmark] '{func.__name__}' executed in {duration * 1000:.3f} ms")
        return result

    return wrapper


def demonstrate_epoch_and_structures() -> None:
    """
    Demonstrate epoch timestamps, human-readable representations, and struct_time objects.
    """
    print("=" * 60)
    print("1. UNIX EPOCH AND STRUCT_TIME")
    print("=" * 60)

    # Current time in seconds since January 1, 1970 00:00:00 UTC (Epoch)
    current_epoch = time.time()
    print(f"  Current Epoch Seconds:         {current_epoch:.6f}")

    # Human-readable string representation
    current_readable = time.ctime(current_epoch)
    print(f"  Current Local Time (ctime):    {current_readable}")

    # Arbitrary epoch conversion (e.g. historical timestamp)
    sample_epoch = 1613004173.957986
    converted_sample = time.ctime(sample_epoch)
    print(f"  Sample Epoch ({sample_epoch}) -> {converted_sample}")

    # Breakdown into struct_time (UTC vs Local)
    utc_struct = time.gmtime(current_epoch)
    local_struct = time.localtime(current_epoch)
    print(f"  UTC Struct Time:   Year={utc_struct.tm_year}, Month={utc_struct.tm_mon}, Day={utc_struct.tm_mday}, Hour={utc_struct.tm_hour}")
    print(f"  Local Struct Time: Year={local_struct.tm_year}, Month={local_struct.tm_mon}, Day={local_struct.tm_mday}, Hour={local_struct.tm_hour}")
    print()


def demonstrate_formatting_and_parsing() -> None:
    """
    Demonstrate formatting struct_time into custom strings (strftime) and parsing (strptime).
    """
    print("=" * 60)
    print("2. STRFTIME AND STRPTIME CONVERSIONS")
    print("=" * 60)

    current_local = time.localtime()

    # Formatting struct_time to custom string
    formatted_iso = time.strftime("%Y-%m-%d %H:%M:%S %Z", current_local)
    formatted_textual = time.strftime("%A, %d %B %Y", current_local)
    print(f"  Formatted ISO 8601:            {formatted_iso}")
    print(f"  Formatted Textual:             {formatted_textual}")

    # Parsing string back into struct_time
    date_str = "2026-10-26 15:45:00"
    parsed_time = time.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    print(f"  Parsed '{date_str}' -> struct_time(year={parsed_time.tm_year}, month={parsed_time.tm_mon}, day={parsed_time.tm_mday})")
    print()


def demonstrate_benchmarking_and_precision() -> None:
    """
    Demonstrate high-precision monotonic timing using perf_counter and sleep.
    """
    print("=" * 60)
    print("3. PRECISION BENCHMARKING (time.perf_counter)")
    print("=" * 60)
    print("  [NOTE] Use time.perf_counter() for benchmarking instead of time.time()")
    print("         because perf_counter() is monotonic and immune to system clock updates.")
    print()

    # Using the BenchmarkTimer context manager
    with BenchmarkTimer("Summation of 1,000,000 integers"):
        total = sum(range(1_000_000))

    # Using the @benchmark decorator
    @benchmark
    def simulated_computation(size: int) -> int:
        return sum(i * i for i in range(size))

    simulated_computation(250_000)

    # Delays and sleep pacing
    print("\n  Demonstrating calibrated delay with time.sleep(0.05):")
    start_delay = time.perf_counter()
    time.sleep(0.05)
    actual_delay = time.perf_counter() - start_delay
    print(f"  Target sleep: 50.00 ms | Actual sleep: {actual_delay * 1000:.2f} ms")
    print()


def main() -> None:
    """Entry point for executing time operations demonstrations."""
    print("PYTHON TIME & PERFORMANCE BENCHMARKING SHOWCASE")
    print()

    demonstrate_epoch_and_structures()
    demonstrate_formatting_and_parsing()
    demonstrate_benchmarking_and_precision()


if __name__ == "__main__":
    main()