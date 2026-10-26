# Python Projects & Practice Repository

A curated collection of Python scripts, categorized by application domain: games & 3D simulations, data science & machine learning examples, foundational language exercises, and supporting multimedia assets.

---

## 📂 Project Structure

```
.
├── audio/            # Sound effects (.wav) and background music assets
├── basics/           # Python fundamental concepts and syntax practice
├── data_science/     # NumPy, Pandas, Matplotlib, and Machine Learning algorithms
├── dsa/              # College & university Data Structures & Algorithms lab programs
├── games/            # 2D and 3D games and physics simulations (Ursina, Pygame)
└── text_files/       # Sample text data files
```

---

## 📁 Directory Overview

### 🎓 [`dsa/`](./dsa)
Complete university-level Data Structures and Algorithms (DSA) laboratory experiments:
- **Searching**: Linear search, Sentinel search, Binary search (iterative, recursive, bounds), Jump search, Ternary search.
- **Sorting**: Bubble sort (early exit), Selection sort, Insertion sort, Merge sort (divide & conquer, inversion counting), Quick sort (Lomuto & Hoare), Heap sort, Counting sort, Radix sort.
- **Stacks**: Stack ADT (Array & Linked List), Infix to Postfix/Prefix, Postfix/Prefix evaluation, Balanced parentheses validator, Two stacks in one array.
- **Queues**: Linear queue (Array & Linked List), Circular queue, Double-Ended Queue (Deque), Binary Min-Heap Priority queue.
- **Linked Lists**: Singly linked list (with cycle detection & merging), Doubly linked list, Circular linked list, Polynomial addition & multiplication.
- **Trees**: Binary tree traversals (DFS recursive/iterative & BFS level order), Binary Search Tree (3-case deletion), AVL Tree (self-balancing LL/RR/LR/RL), Min/Max Heaps.
- **Graphs**: Matrix & List representations, BFS & DFS, Kahn's Topological sort, Dijkstra's shortest path, Bellman-Ford, Floyd-Warshall, Prim's MST, Kruskal's MST (Union-Find).
- **Hashing**: Separate chaining with dynamic rehashing, Open addressing (Linear, Quadratic, Double hashing with tombstones).
- **Classic Algorithms**: 0/1 & Fractional Knapsack, Longest Common Subsequence (LCS), Matrix Chain Multiplication (MCM), N-Queens (Backtracking), Huffman Coding.
- **Interactive Runner**: Launch `python dsa/dsa_runner.py` for an interactive menu or to run the 43-test suite.

### 🎮 [`games/`](./games)
Interactive games, 2D arcade classics, and progressive 3D prototype versions:
- **3D Progressive Builds (`3d_1.0.py` – `3d_1.9.py`, `Fixed Script (3d_1.3).py`)**: 3D prototype iterations powered by the [Ursina](https://www.ursinaspaces.org/) engine, featuring first-person controls, procedural sound synthesis, coin collection, and multiple weapon types.
- **`space_fighter.py`**: 3D space shooter simulation with procedurally synthesized audio, laser projectile mechanics, particle explosions, and enemy wave spawning.
- **Pac-Man Implementations**:
  - `pacman.py`: Classic arcade maze navigation and ghost logic.
  - `Pacman_Gemini.py`: Pygame-based Pac-Man implementation with sound effects and animations.
  - `pacman_Github_copilot.py`: Clean maze navigation variant.
- **`mario.py`**: Retro 2D platformer with running, jumping physics, platforms, collectibles, and enemy collision.
- **`Snake_Game.py`**: Grid-based classic Snake arcade game built with Pygame.
- **`neon_shift_main.py`**: Fast-paced synthwave-themed obstacle runner with audio effects.
- **`particles.py`**: Interactive 2D physics particle fountain responding to real-time mouse inputs.
- **`newcopilotgame.py`**: 2D arcade game experiment.

### 📊 [`data_science/`](./data_science)
Data manipulation, numerical computation, visualization, and ML implementations:
- **NumPy & Arrays**:
  - `numpy_array_creation.py`, `numpy_data_types.py`, `numpy_basic_operations.py`, `numpy_math_operations.py`, `numpy_array_indexing.py`, `numpy_array_formatting.py`
- **Pandas & DataFrames**:
  - `pandas_series_from_list.py`, `pandas_dataframe_from_dict.py`, `pandas_dataframe_exploration.py`, `pandas_read_csv_json.py`
- **Machine Learning**:
  - `kmeans_clustering.py`: Unsupervised clustering example using scikit-learn.
  - `logistic_regression.py`: Binary classification model with train/test splitting and accuracy evaluation.
- **Data Visualization & Stats**:
  - `matplotlib_visualization.py`: Line and bar chart creation with Matplotlib.
  - `statistics_operations.py`: Calculations with Python's built-in `statistics` module (mean, median, mode, stdev).

### 🐍 [`basics/`](./basics)
Core Python language fundamentals, clean coding idioms, and standard library demonstrations:
- **`variables_and_types.py`**: Dynamic typing, primitive data types, memory identity (`is` vs `==`), mutability, and type casting.
- **`print_formatting.py`**: `print()` parameter controls (`sep`, `end`, `file`), modern f-strings, format specifiers, and alignment.
- **`function_basics.py`**: Pure functions, type annotations, positional/keyword/keyword-only arguments, `*args`, `**kwargs`, closures, and lambdas.
- **`list_operations.py`**: Indexing, forward/negative slicing, in-place mutations, sorting, copying, comprehensions, and iteration idioms.
- **`tuple_operations.py`**: Immutability, memory efficiency, sequence slicing, unpacking, hashability, and `typing.NamedTuple`.
- **`file_handling.py`**: Cross-platform path management with `pathlib.Path`, context managers (`with`), streaming generators, and safe exception handling.
- **`math_operations.py`**: Number theory (`gcd`, `lcm`, `factorial`), powers, logarithms, trigonometry, precision comparisons (`isclose`), and mathematical constants.
- **`random_operations.py`**: Pseudo-random number generation, sequence sampling, weighted selections, distributions, and security considerations (`secrets` module).
- **`time_operations.py`**: UNIX epoch timestamps, `strftime`/`strptime` conversions, and monotonic high-resolution benchmarking (`time.perf_counter()`).
- **`prime_numbers.py`**: Optimized primality testing (6k ± 1 trial division), Sieve of Eratosthenes ($O(n \log \log n)$), and prime factorization.

### 🔊 [`audio/`](./audio)
Sound effects and background music in uncompressed 16-bit PCM WAV format used across the games:
- **Background Music**: `bgm.wav`, `bg_music.wav`
- **Sound Effects**: `coin.wav`, `explosion_snd.wav`, `hit_snd.wav`, `jump.wav`, `laser_snd.wav`, `reload.wav`, `shoot.wav`, `shoot_pistol.wav`, `shoot_shotgun.wav`, `shoot_smg.wav`, `switch.wav`

### 📄 [`text_files/`](./text_files)
- **`days.txt`**: Sample plaintext line data for string and iteration exercises.
- **`data.txt`**: Sample multi-line text used for file I/O operations (`open`, `read`, `write`).
- **`people.csv`**: Sample tabular dataset with demographic records for Pandas CSV parsing exercises.

---

## 🚀 Getting Started

### Prerequisites & Installation

Python 3.9+ is recommended. Install all repository dependencies via `requirements.txt`:

```bash
pip install -r requirements.txt
```


### Running Scripts

Execute scripts directly with Python:

```bash
# Run the interactive DSA Lab menu or test suite
python dsa/dsa_runner.py

# Run a game
python games/Snake_Game.py
python games/space_fighter.py

# Run a data science script
python data_science/logistic_regression.py

# Run a basics exercise
python basics/prime_numbers.py
```
