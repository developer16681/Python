"""
File Handling and I/O Operations in Python
=========================================

This module demonstrates safe, idiomatic, and robust file input/output (I/O)
operations in Python, leveraging pathlib.Path, context managers, and explicit encoding.

Key Concepts Covered:
---------------------
1. Cross-platform path management with pathlib.Path
2. Deterministic resource management using 'with open(...) as file:'
3. Explicit character encoding (UTF-8 standard)
4. Reading patterns: whole file, streaming line-by-line, and readlines()
5. Writing and appending patterns: overwrite mode ('w') vs. append mode ('a')
6. Defensive error handling (FileNotFoundError, PermissionError, OSError)
7. Temporary demonstration file lifecycle and cleanup
"""

import os
from pathlib import Path
from typing import Generator, List, Optional


def resolve_repository_data_file() -> Optional[Path]:
    """
    Locate the sample data file within the repository structure.

    Returns:
        Path object to the data file if it exists, otherwise None.
    """
    repo_root = Path(__file__).resolve().parent.parent
    candidate_paths: List[Path] = [
        repo_root / "text_files" / "data.txt",
        Path("text_files") / "data.txt",
        Path("data.txt"),
    ]

    for candidate in candidate_paths:
        if candidate.is_file():
            return candidate
    return None


def read_entire_file(file_path: Path) -> str:
    """
    Read the complete content of a UTF-8 encoded text file.

    Args:
        file_path: Target Path to read.

    Returns:
        String content of the file.

    Raises:
        FileNotFoundError: If the specified path does not exist.
    """
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, mode="r", encoding="utf-8") as file:
        return file.read()


def stream_lines(file_path: Path) -> Generator[str, None, None]:
    """
    Memory-efficient generator that yields lines one-by-one from a text file.
    Ideal for large log files or large datasets without loading them all into RAM.

    Args:
        file_path: Target Path to read.

    Yields:
        Stripped string for each line.
    """
    with open(file_path, mode="r", encoding="utf-8") as file:
        for line in file:
            yield line.rstrip("\r\n")


def write_text_file(file_path: Path, lines: List[str], append: bool = False) -> int:
    """
    Write or append lines to a file with newline delimiters.

    Args:
        file_path: Target Path destination.
        lines: Sequence of string lines to persist.
        append: If True, open in append mode ('a'); otherwise overwrite ('w').

    Returns:
        Total number of characters written.
    """
    mode = "a" if append else "w"
    chars_written = 0

    with open(file_path, mode=mode, encoding="utf-8") as file:
        for line in lines:
            chars_written += file.write(line + "\n")

    return chars_written


def demonstrate_safe_error_handling() -> None:
    """
    Demonstrate professional exception handling when interacting with the filesystem.
    """
    print("=" * 60)
    print("1. DEFENSIVE FILE SYSTEM ERROR HANDLING")
    print("=" * 60)

    non_existent = Path("non_existent_directory") / "missing_file.txt"
    try:
        read_entire_file(non_existent)
    except FileNotFoundError as err:
        print(f"  Gracefully handled missing file: {err}")
    except PermissionError as err:
        print(f"  Gracefully handled permission failure: {err}")
    except OSError as err:
        print(f"  Operating system I/O error: {err}")
    print()


def demonstrate_reading_existing_data() -> None:
    """
    Read and display data from the repository's text_files/data.txt.
    """
    print("=" * 60)
    print("2. READING REPOSITORY DATA ASSET")
    print("=" * 60)

    data_file = resolve_repository_data_file()
    if data_file:
        print(f"  Target File: {data_file}")
        content = read_entire_file(data_file)
        print("  File Content Snippet:")
        # Print first few lines
        lines = content.strip().splitlines()
        for idx, line in enumerate(lines[:5], start=1):
            print(f"    Line {idx}: {line}")
        if len(lines) > 5:
            print(f"    ... and {len(lines) - 5} more lines.")
    else:
        print("  Sample data file not found in default paths.")
    print()


def demonstrate_file_write_and_stream() -> None:
    """
    Demonstrate creating, appending, and streaming from a temporary text file.
    """
    print("=" * 60)
    print("3. WRITE, APPEND, AND STREAMING ITERATION")
    print("=" * 60)

    demo_path = Path(__file__).resolve().parent / "demo_output.tmp"
    initial_content = [
        "[INFO] System initialized.",
        "[INFO] Database connection established.",
        "[WARNING] High memory usage detected.",
    ]

    try:
        # Write initial records
        written = write_text_file(demo_path, initial_content, append=False)
        print(f"  Created '{demo_path.name}' ({written} characters written).")

        # Append additional records
        append_content = [
            "[INFO] Garbage collection executed.",
            "[INFO] Service listening on port 8080.",
        ]
        appended = write_text_file(demo_path, append_content, append=True)
        print(f"  Appended to '{demo_path.name}' ({appended} characters appended).")

        # Stream lines one by one
        print("\n  Streaming lines via generator (memory-efficient):")
        for line_no, record in enumerate(stream_lines(demo_path), start=1):
            print(f"    [{line_no:02d}] {record}")

    finally:
        # Clean up temporary demonstration file
        if demo_path.exists():
            demo_path.unlink()
            print(f"\n  Cleanup: Successfully removed temporary file '{demo_path.name}'.")
    print()


def main() -> None:
    """Entry point for demonstrating file handling patterns."""
    print("PYTHON FILE HANDLING & STREAM I/O SHOWCASE")
    print()

    demonstrate_safe_error_handling()
    demonstrate_reading_existing_data()
    demonstrate_file_write_and_stream()


if __name__ == "__main__":
    main()
