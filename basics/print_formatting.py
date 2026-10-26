"""
Print Function and String Formatting in Python
==============================================

This module demonstrates idiomatic text output and string formatting techniques
in modern Python, ranging from standard console I/O options to advanced f-strings.

Key Concepts Covered:
---------------------
1. print() parameter controls: sep, end, flush, and file redirection
2. Modern f-strings (PEP 498): expressions, format specifiers, alignment
3. Self-documenting f-strings ({var=} syntax, Python 3.8+)
4. str.format() method & positional/named arguments
5. Legacy %-formatting comparison
6. Raw strings, escape characters, and multi-line strings
"""

import math
import sys
from datetime import datetime


def demonstrate_print_parameters() -> None:
    """
    Demonstrate custom arguments of the built-in print() function:
    print(*objects, sep=' ', end='\\n', file=sys.stdout, flush=False)
    """
    print("=" * 60)
    print("1. BUILT-IN PRINT() FUNCTION ARGUMENTS")
    print("=" * 60)

    # Custom separator (default is a single space)
    print("  Default separator:", "apple", "banana", "cherry")
    print("  Custom separator :", "apple", "banana", "cherry", sep=" | ")
    print("  CSV format       :", "John", "Doe", "30", "Developer", sep=", ")

    # Custom line termination (default is newline '\n')
    print("  Progress count: ", end="")
    for i in range(1, 6):
        print(f"[{i}]", end=" ", flush=True)
    print("Done!\n")

    # Writing to standard error stream
    print("  Notice: Diagnostics stream output.", file=sys.stderr)
    print()


def demonstrate_fstring_formatting() -> None:
    """
    Demonstrate formatted string literals (f-strings) with alignment,
    numerical precision, thousands separators, and debugging expressions.
    """
    print("=" * 60)
    print("2. MODERN F-STRING FORMATTING")
    print("=" * 60)

    item_name: str = "Mechanical Keyboard"
    unit_price: float = 129.99
    quantity: int = 3
    total_cost: float = unit_price * quantity
    discount_rate: float = 0.15

    # Basic variable interpolation and embedded arithmetic
    print(f"  Item: {item_name} (Qty: {quantity})")
    print(f"  Unit Price: ${unit_price:.2f} | Subtotal: ${total_cost:.2f}")
    print(f"  Discount ({discount_rate:.0%}): -${total_cost * discount_rate:.2f}")
    print(f"  Final Amount: ${total_cost * (1 - discount_rate):,.2f}")

    # Self-documenting expressions (Python 3.8+)
    print("\n  Self-Documenting Debugging Syntax ({var=}):")
    radius: float = 5.0
    area: float = math.pi * (radius ** 2)
    print(f"  {radius=}, {area=:.4f}")

    # Text Alignment and Padding (:^ center, :< left, :> right)
    print("\n  Alignment and Padding Demo:")
    headers = ("ID", "Product Name", "Price")
    print(f"  {headers[0]:<6} | {headers[1]:<25} | {headers[2]:>10}")
    print("  " + "-" * 47)
    sample_items = [
        (101, "Wireless Mouse", 24.50),
        (102, "4K Monitor 27-inch", 389.00),
        (103, "USB-C Cable (2m)", 9.99),
    ]
    for item_id, name, price in sample_items:
        print(f"  {item_id:<6} | {name:<25} | ${price:>9.2f}")
    print()


def demonstrate_datetime_and_number_formatting() -> None:
    """
    Demonstrate number radix formatting (binary, hex, octal) and date formatting.
    """
    print("=" * 60)
    print("3. RADIX & DATE FORMAT SPECIFIERS")
    print("=" * 60)

    number: int = 255
    print(f"  Decimal:     {number:d}")
    print(f"  Binary:      {number:08b} (padded to 8 bits)")
    print(f"  Hexadecimal: {number:#04x} (with prefix)")
    print(f"  Octal:       {number:#04o}")

    now = datetime(2026, 10, 26, 15, 30, 0)
    print(f"  Custom Date: {now:%Y-%m-%d %H:%M:%S}")
    print(f"  Locale Date: {now:%B %d, %Y}")
    print()


def demonstrate_alternative_formatting() -> None:
    """
    Compare modern f-strings with str.format() and legacy %-formatting.
    """
    print("=" * 60)
    print("4. STR.FORMAT() AND LEGACY %-FORMATTING")
    print("=" * 60)

    name = "Dev"
    role = "Software Architect"

    # str.format()
    msg_str_format = "  [str.format] User: {} | Role: {}".format(name, role)
    print(msg_str_format)

    # Named placeholders with str.format()
    template = "  [str.format named] User: {user_name} (Permissions: {perm})"
    print(template.format(user_name=name, perm="Admin"))

    # Legacy % printf-style formatting
    legacy_msg = "  [Legacy %%]   User: %s | Role: %s" % (name, role)
    print(legacy_msg)
    print()


def main() -> None:
    """Entry point for executing string and print formatting demonstrations."""
    print("PYTHON CONSOLE I/O & FORMATTING SHOWCASE")
    print()

    demonstrate_print_parameters()
    demonstrate_fstring_formatting()
    demonstrate_datetime_and_number_formatting()
    demonstrate_alternative_formatting()


if __name__ == "__main__":
    main()