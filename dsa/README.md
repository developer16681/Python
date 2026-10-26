# 🎓 College & University Data Structures and Algorithms (DSA) Lab Repository

A complete, production-grade collection of **essential Data Structures & Algorithms lab programs** in Python, mapped directly to standard Computer Science and Information Technology university lab curricula (ABET, AICTE, Anna University, VTU, Mumbai University, AKTU, SPPU, Delhi University, etc.).

Each program includes:
- **Formal Lab Aim & Theory**
- **Comprehensive Step-by-Step Algorithms**
- **Time Complexity** (Best, Average, Worst) and **Space Complexity** Analysis
- **Edge-case Handling & Visual Step Tracing**
- Standalone execution via `if __name__ == '__main__':`

---

## 🚀 Quick Start: Running the Lab Suite

### Interactive Menu & Automated Test Suite
An interactive console runner is provided at [`dsa/dsa_runner.py`](./dsa_runner.py).

To launch the interactive menu:
```bash
python dsa/dsa_runner.py
```

To run all 43 lab experiment test suites automatically:
```bash
python -c "import dsa.dsa_runner as r; r.run_all_tests()"
```

Or execute any experiment individually:
```bash
python dsa/01_searching/binary_search.py
python dsa/03_stacks/infix_to_postfix_and_prefix.py
python dsa/06_trees/avl_tree.py
python dsa/07_graphs/dijkstra_shortest_path.py
```

---

## 📚 Curriculum & Experiment Index

### 1. 🔍 Searching Algorithms (`dsa/01_searching/`)
| Experiment | Script | Time Complexity (Avg/Worst) | Space Complexity | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Linear Search** | [`linear_search.py`](./01_searching/linear_search.py) | $O(n)$ / $O(n)$ | $O(1)$ | Standard linear search, sentinel search optimization, multi-occurrence reporting, visual index tracing. |
| **Binary Search** | [`binary_search.py`](./01_searching/binary_search.py) | $O(\log n)$ / $O(\log n)$ | $O(1)$ iter, $O(\log n)$ rec | Iterative and recursive implementations, lower/upper bounds (first & last occurrences), window tracing. |
| **Jump & Ternary Search** | [`jump_and_ternary_search.py`](./01_searching/jump_and_ternary_search.py) | $O(\sqrt{n})$ / $O(\log_3 n)$ | $O(1)$ | Block jumping with step $m = \sqrt{n}$ and 3-way partition ternary search. |

---

### 2. 🔀 Sorting Algorithms (`dsa/02_sorting/`)
| Experiment | Script | Time Complexity (Best / Avg / Worst) | Space | Stability | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Bubble Sort** | [`bubble_sort.py`](./02_sorting/bubble_sort.py) | $O(n)$ / $O(n^2)$ / $O(n^2)$ | $O(1)$ | Stable | Adjacent comparison with `swapped` early-termination flag and pass logging. |
| **Selection Sort** | [`selection_sort.py`](./02_sorting/selection_sort.py) | $O(n^2)$ / $O(n^2)$ / $O(n^2)$ | $O(1)$ | Unstable | Subarray minimum identification and swap tracing. |
| **Insertion Sort** | [`insertion_sort.py`](./02_sorting/insertion_sort.py) | $O(n)$ / $O(n^2)$ / $O(n^2)$ | $O(1)$ | Stable | Card-sorting analogy with rightward element shifts. |
| **Merge Sort** | [`merge_sort.py`](./02_sorting/merge_sort.py) | $O(n \log n)$ across all cases | $O(n)$ | Stable | Divide-and-conquer recursive partitioning, merging, and array inversion counter. |
| **Quick Sort** | [`quick_sort.py`](./02_sorting/quick_sort.py) | $O(n \log n)$ / $O(n \log n)$ / $O(n^2)$ | $O(\log n)$ | Unstable | Lomuto and Hoare partitioning schemes with recursion tree tracing. |
| **Heap Sort** | [`heap_sort.py`](./02_sorting/heap_sort.py) | $O(n \log n)$ across all cases | $O(1)$ | Unstable | Binary Max-Heap construction, sift-down heapify, and root extraction. |
| **Counting & Radix Sort** | [`counting_and_radix_sort.py`](./02_sorting/counting_and_radix_sort.py) | $O(n + k)$ / $O(d(n + b))$ | $O(n + k)$ | Stable | Non-comparison linear sorting and digit-by-digit LSD Radix sorting. |

---

### 3. 🥞 Stacks (`dsa/03_stacks/`)
| Experiment | Script | Key Operations | Description |
| :--- | :--- | :--- | :--- |
| **Stack ADT (Array)** | [`stack_array.py`](./03_stacks/stack_array.py) | `push`, `pop`, `peek`, `is_empty`, `is_full` | Fixed-capacity array implementation with custom overflow and underflow exception classes. |
| **Stack ADT (Linked List)** | [`stack_linked_list.py`](./03_stacks/stack_linked_list.py) | `push`, `pop`, `peek`, `size` | Dynamic memory allocation using singly linked list nodes. |
| **Infix to Postfix & Prefix** | [`infix_to_postfix_and_prefix.py`](./03_stacks/infix_to_postfix_and_prefix.py) | Shunting-Yard conversion | Operator precedence (`^`, `*`, `/`, `%`, `+`, `-`), associativity, parentheses handling, step-by-step conversion table. |
| **Postfix & Prefix Evaluation** | [`postfix_prefix_evaluation.py`](./03_stacks/postfix_prefix_evaluation.py) | Expression evaluator | Stack evaluation for multi-digit operands and standard operators. |
| **Balanced Parentheses** | [`balanced_parentheses.py`](./03_stacks/balanced_parentheses.py) | Delimiter validation | Syntax checker for `()`, `{}`, `[]` with exact error location and reason reporting. |
| **Two Stacks in One Array** | [`two_stacks_in_one_array.py`](./03_stacks/two_stacks_in_one_array.py) | Bidirectional stack growth | Memory-efficient dual stacks starting from index $0$ and $n-1$. |

---

### 4. 🚶‍♂️ Queues (`dsa/04_queues/`)
| Experiment | Script | Complexity | Description |
| :--- | :--- | :--- | :--- |
| **Linear Queue** | [`linear_queue.py`](./04_queues/linear_queue.py) | $O(1)$ ops | Array-based and linked-list-based FIFO queue. |
| **Circular Queue** | [`circular_queue.py`](./04_queues/circular_queue.py) | $O(1)$ ops | Modulo arithmetic `(rear + 1) % capacity == front` eliminating memory drift. |
| **Double-Ended Queue (Deque)** | [`deque.py`](./04_queues/deque.py) | $O(1)$ ops | Circular array buffer supporting insertions and deletions at both ends. |
| **Priority Queue** | [`priority_queue.py`](./04_queues/priority_queue.py) | $O(\log n)$ insert/extract | Binary Min-Heap priority queue serving highest priority elements first. |

---

### 5. 🔗 Linked Lists (`dsa/05_linked_lists/`)
| Experiment | Script | Methods Implemented | Description |
| :--- | :--- | :--- | :--- |
| **Singly Linked List** | [`singly_linked_list.py`](./05_linked_lists/singly_linked_list.py) | Insert/Delete (head, tail, index, value), Reverse (iter & rec), Detect Loop, Merge Sorted | Complete singly linked list suite with Floyd's Cycle Detection and sorted list merging. |
| **Doubly Linked List** | [`doubly_linked_list.py`](./05_linked_lists/doubly_linked_list.py) | `prev` and `next` pointers, forward & backward traversal | Insertion and deletion at head and tail with bidirectional links. |
| **Circular Linked List** | [`circular_linked_list.py`](./05_linked_lists/circular_linked_list.py) | Circular insertion, deletion, split | Maintained with `last` pointer; includes splitting into two circular halves. |
| **Polynomial Addition & Multiplication** | [`polynomial_addition.py`](./05_linked_lists/polynomial_addition.py) | Term merge, add, multiply, algebraic format | Classic university lab experiment representing polynomials as linked nodes ($c \cdot x^e$). |

---

### 6. 🌳 Trees (`dsa/06_trees/`)
| Experiment | Script | Key Features |
| :--- | :--- | :--- |
| **Binary Tree Traversals** | [`binary_tree_traversals.py`](./06_trees/binary_tree_traversals.py) | Recursive & iterative Inorder, Preorder, Postorder; Level-Order (BFS); Tree Height, Node Count, Leaf Count. |
| **Binary Search Tree (BST)** | [`binary_search_tree.py`](./06_trees/binary_search_tree.py) | Insertion, search, 3-case node deletion (leaf, 1 child, 2 children with inorder successor), Min/Max, ASCII visualizer. |
| **AVL Tree (Self-Balancing BST)** | [`avl_tree.py`](./06_trees/avl_tree.py) | Balance factor maintenance, Left-Left (LL), Right-Right (RR), Left-Right (LR), Right-Left (RL) rotations, ASCII tree display. |
| **Min-Heap & Max-Heap** | [`min_max_heap.py`](./06_trees/min_max_heap.py) | Array-based binary heap arithmetic ($2i+1, 2i+2, (i-1)//2$), sift-up, sift-down, extract root. |

---

### 7. 🕸️ Graphs (`dsa/07_graphs/`)
| Experiment | Script | Complexity | Description |
| :--- | :--- | :--- | :--- |
| **Graph Representations** | [`graph_representations.py`](./07_graphs/graph_representations.py) | $O(V^2)$ vs $O(V+E)$ | Adjacency Matrix and Adjacency List for directed and undirected graphs. |
| **BFS & DFS Traversals** | [`bfs_dfs_traversal.py`](./07_graphs/bfs_dfs_traversal.py) | $O(V + E)$ | Breadth-First Search, Depth-First Search (recursive & iterative), connected components. |
| **Topological Sort** | [`topological_sort.py`](./07_graphs/topological_sort.py) | $O(V + E)$ | Kahn's algorithm (BFS in-degrees) and DFS-based topological sort with cycle detection. |
| **Dijkstra's Algorithm** | [`dijkstra_shortest_path.py`](./07_graphs/dijkstra_shortest_path.py) | $O((V+E)\log V)$ | Single-source shortest path using Min-Heap priority queue and path reconstruction. |
| **Bellman-Ford Algorithm** | [`bellman_ford.py`](./07_graphs/bellman_ford.py) | $O(V \cdot E)$ | Single-source shortest path supporting negative edge weights and negative cycle detection. |
| **Floyd-Warshall Algorithm** | [`floyd_warshall.py`](./07_graphs/floyd_warshall.py) | $O(V^3)$ | All-pairs shortest path dynamic programming algorithm. |
| **Prim's Algorithm (MST)** | [`prims_mst.py`](./07_graphs/prims_mst.py) | $O((V+E)\log V)$ | Greedy vertex-growing Minimum Spanning Tree using priority queue. |
| **Kruskal's Algorithm (MST)** | [`kruskals_mst.py`](./07_graphs/kruskals_mst.py) | $O(E \log E)$ | Greedy edge-selection Minimum Spanning Tree using Disjoint Set Union (DSU / Union-Find). |

---

### 8. 🗄️ Hashing (`dsa/08_hashing/`)
| Experiment | Script | Techniques Implemented | Description |
| :--- | :--- | :--- | :--- |
| **Separate Chaining** | [`hash_table_chaining.py`](./08_hashing/hash_table_chaining.py) | Linked list buckets, load factor monitoring ($\alpha = n/m$), dynamic rehashing. | Clean collision resolution by chaining linked nodes at each bucket. |
| **Open Addressing** | [`hash_table_open_addressing.py`](./08_hashing/hash_table_open_addressing.py) | Linear Probing, Quadratic Probing, Double Hashing, `DELETED` tombstones. | Probing algorithms with tombstone marker preservation during deletions. |

---

### 9. 🧠 Classic Algorithmic Lab Problems (`dsa/09_classic_algorithms/`)
| Experiment | Script | Paradigm | Description |
| :--- | :--- | :--- | :--- |
| **0/1 & Fractional Knapsack** | [`knapsack_01_and_fractional.py`](./09_classic_algorithms/knapsack_01_and_fractional.py) | Dynamic Programming & Greedy | Comparison of 0/1 knapsack (DP table & item backtracking) vs fractional knapsack ($v/w$ greedy ratio). |
| **Longest Common Subsequence (LCS)** | [`longest_common_subsequence.py`](./09_classic_algorithms/longest_common_subsequence.py) | Dynamic Programming | Computes LCS length, displays full 2D DP matrix, and reconstructs the optimal subsequence string. |
| **Matrix Chain Multiplication (MCM)** | [`matrix_chain_multiplication.py`](./09_classic_algorithms/matrix_chain_multiplication.py) | Dynamic Programming | Computes minimum scalar multiplications and outputs fully parenthesized matrix formulas. |
| **N-Queens Problem** | [`n_queens_backtracking.py`](./09_classic_algorithms/n_queens_backtracking.py) | Backtracking | Finds all non-attacking queen configurations on an $N \times N$ chessboard with ASCII boards. |
| **Huffman Coding** | [`huffman_coding.py`](./09_classic_algorithms/huffman_coding.py) | Greedy Compression | Min-Heap frequency tree construction, prefix code generation, message encoding, and bitstream decoding. |
