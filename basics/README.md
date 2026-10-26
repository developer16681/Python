# 🐍 Python Basics & Core Language Fundamentals

A production-grade, curated reference guide and practice suite covering core Python language fundamentals, syntax patterns, data structures, and standard library modules.

All scripts in this directory follow **PEP 8** style guidelines, leverage explicit **PEP 484 type hints**, provide **PEP 257 docstrings**, and include self-documenting execution entry points under `if __name__ == "__main__":`.

---

## 📂 Module Catalog

| Module | Primary Focus | Key Concepts & Functions Covered |
| :--- | :--- | :--- |
| [`variables_and_types.py`](./variables_and_types.py) | Dynamic Typing & Object Model | Scalar types (`int`, `float`, `complex`, `bool`, `str`, `NoneType`), collections overview, object identity (`id()`, `is` vs `==`), mutability vs immutability, and truth value testing (truthiness). |
| [`print_formatting.py`](./print_formatting.py) | Output & String Formatting | Built-in `print()` arguments (`sep`, `end`, `file`, `flush`), modern f-strings (PEP 498), number radix formatting (`:08b`, `:#04x`), text alignment, dates, `str.format()`, and legacy `%`-formatting. |
| [`function_basics.py`](./function_basics.py) | Function Design & Call Signatures | Pure functions, type annotations, positional-only (`/`) and keyword-only (`*`) parameters, variadic arguments (`*args`, `**kwargs`), tuple unpacking returns, higher-order functions, and closures. |
| [`list_operations.py`](./list_operations.py) | Mutable Sequences & Slicing | Indexing, slicing notations (`[start:stop:step]`, `[::-1]`), in-place mutation (`append`, `extend`, `insert`, `pop`, `remove`), custom sorting, shallow vs deep copying (`copy` module), and list comprehensions. |
| [`tuple_operations.py`](./tuple_operations.py) | Immutable Sequences & Records | Singleton comma syntax gotcha, immutability guarantees, memory footprint comparisons (`sys.getsizeof`), tuple unpacking, dictionary hash keys, and structured records with `typing.NamedTuple`. |
| [`file_handling.py`](./file_handling.py) | File I/O & Stream Processing | Path resolution using `pathlib.Path`, deterministic context managers (`with open(...)`), explicit UTF-8 encoding, streaming generators for large datasets, and defensive exception handling (`FileNotFoundError`). |
| [`math_operations.py`](./math_operations.py) | Numerical & Standard Library Math | Number theory (`gcd`, `lcm`, `factorial`, `isqrt`, combinatorics), powers, logarithms, trigonometry, precision comparisons (`math.isclose`), and mathematical constants (`pi`, `e`, `tau`, `inf`, `nan`). |
| [`random_operations.py`](./random_operations.py) | PRNG & Sampling | Pseudo-random scalars (`uniform`, `randint`, `randrange`), sequence sampling (`choice`, `sample`, `shuffle`), weighted choices (`choices`), reproducibility (`seed`), and CSPRNG security comparison (`secrets`). |
| [`time_operations.py`](./time_operations.py) | Time & Performance Benchmarking | UNIX epoch timestamps (`time.time`, `ctime`), `struct_time` representations, `strftime`/`strptime` conversions, and monotonic high-resolution timing using `time.perf_counter()` with custom timer context managers and decorators. |
| [`prime_numbers.py`](./prime_numbers.py) | Algorithms & Number Theory | Optimized $6k \pm 1$ primality trial division ($O(\sqrt{n})$), Sieve of Eratosthenes ($O(n \log \log n)$), first-$N$ prime stream generators, and prime factorization. |

---

## 🚀 Running the Modules

You can execute any module directly from the terminal.

### Run an Individual Exercise

From the repository root:
```powershell
python basics/variables_and_types.py
python basics/print_formatting.py
python basics/function_basics.py
python basics/list_operations.py
python basics/tuple_operations.py
python basics/file_handling.py
python basics/math_operations.py
python basics/random_operations.py
python basics/time_operations.py
python basics/prime_numbers.py
```

Or from inside the `basics/` folder:
```powershell
cd basics
python list_operations.py
```

### Run All Modules in Sequence

To run all basic practice modules and verify execution status:

```powershell
Get-ChildItem -Filter *.py | ForEach-Object { python $_.Name }
```

---

## 🛠️ Code Conventions & Standards

- **Naming Conventions**: Modules, functions, and variables use `snake_case`. Constants use `UPPER_CASE`.
- **Zero Namespace Collision**: No files shadow Python keywords (e.g. `def`) or standard library modules (e.g. `math`, `time`, `list`, `tuple`).
- **Defensive Design**: Built with error handling, bounds checking, and predictable return types.
- **Cross-Platform Compatibility**: Fully compatible with Windows (PowerShell/CMD), Linux, and macOS without encoding or terminal formatting issues.
