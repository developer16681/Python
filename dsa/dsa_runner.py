"""
College/University DSA Lab Interactive Runner & Test Suite
-----------------------------------------------------------
This interactive utility enables students, instructors, and developers to:
1. Run any specific DSA experiment interactively from a numbered menu.
2. Run an automated test suite across all 25+ DSA lab programs.
3. Inspect complexity and algorithms covered in the lab curriculum.
"""

import os
import subprocess
import sys
from typing import Dict, List, Tuple


EXPERIMENTS: List[Tuple[str, str, str]] = [
    # (Category, Title, Relative Path)
    ("1. Searching", "Linear Search & Sentinel Search", "01_searching/linear_search.py"),
    ("1. Searching", "Binary Search (Iterative, Recursive, Bounds)", "01_searching/binary_search.py"),
    ("1. Searching", "Jump Search & Ternary Search", "01_searching/jump_and_ternary_search.py"),

    ("2. Sorting", "Bubble Sort (with Early Termination Flag)", "02_sorting/bubble_sort.py"),
    ("2. Sorting", "Selection Sort", "02_sorting/selection_sort.py"),
    ("2. Sorting", "Insertion Sort", "02_sorting/insertion_sort.py"),
    ("2. Sorting", "Merge Sort (Divide & Conquer & Inversion Count)", "02_sorting/merge_sort.py"),
    ("2. Sorting", "Quick Sort (Lomuto & Hoare Partitioning)", "02_sorting/quick_sort.py"),
    ("2. Sorting", "Heap Sort (Max-Heapify)", "02_sorting/heap_sort.py"),
    ("2. Sorting", "Counting Sort & Radix Sort (Non-Comparison)", "02_sorting/counting_and_radix_sort.py"),

    ("3. Stacks", "Stack ADT using Array (Fixed Capacity)", "03_stacks/stack_array.py"),
    ("3. Stacks", "Stack ADT using Singly Linked List", "03_stacks/stack_linked_list.py"),
    ("3. Stacks", "Infix to Postfix and Prefix Conversion", "03_stacks/infix_to_postfix_and_prefix.py"),
    ("3. Stacks", "Postfix and Prefix Expression Evaluation", "03_stacks/postfix_prefix_evaluation.py"),
    ("3. Stacks", "Balanced Parentheses / Delimiter Checker", "03_stacks/balanced_parentheses.py"),
    ("3. Stacks", "Two Stacks in a Single Array", "03_stacks/two_stacks_in_one_array.py"),

    ("4. Queues", "Linear Queue (Array & Linked List)", "04_queues/linear_queue.py"),
    ("4. Queues", "Circular Queue (Modulo Arithmetic)", "04_queues/circular_queue.py"),
    ("4. Queues", "Double-Ended Queue (Deque)", "04_queues/deque.py"),
    ("4. Queues", "Priority Queue (Binary Min-Heap)", "04_queues/priority_queue.py"),

    ("5. Linked Lists", "Singly Linked List (Insert, Delete, Reverse, Loop)", "05_linked_lists/singly_linked_list.py"),
    ("5. Linked Lists", "Doubly Linked List (Bidirectional)", "05_linked_lists/doubly_linked_list.py"),
    ("5. Linked Lists", "Circular Singly Linked List & Half-Split", "05_linked_lists/circular_linked_list.py"),
    ("5. Linked Lists", "Polynomial Representation & Operations", "05_linked_lists/polynomial_addition.py"),

    ("6. Trees", "Binary Tree Traversals (Recursive, Iterative, BFS)", "06_trees/binary_tree_traversals.py"),
    ("6. Trees", "Binary Search Tree (BST 3-Case Deletion & Min/Max)", "06_trees/binary_search_tree.py"),
    ("6. Trees", "AVL Tree (Self-Balancing with LL, RR, LR, RL)", "06_trees/avl_tree.py"),
    ("6. Trees", "Binary Min-Heap and Max-Heap Operations", "06_trees/min_max_heap.py"),

    ("7. Graphs", "Graph Representations (Matrix & List)", "07_graphs/graph_representations.py"),
    ("7. Graphs", "BFS & DFS Graph Traversals & Components", "07_graphs/bfs_dfs_traversal.py"),
    ("7. Graphs", "Topological Sort (Kahn's Algorithm & DFS)", "07_graphs/topological_sort.py"),
    ("7. Graphs", "Dijkstra's Shortest Path Algorithm", "07_graphs/dijkstra_shortest_path.py"),
    ("7. Graphs", "Bellman-Ford Algorithm (Negative Weights/Cycles)", "07_graphs/bellman_ford.py"),
    ("7. Graphs", "Floyd-Warshall All-Pairs Shortest Path", "07_graphs/floyd_warshall.py"),
    ("7. Graphs", "Prim's Minimum Spanning Tree", "07_graphs/prims_mst.py"),
    ("7. Graphs", "Kruskal's Minimum Spanning Tree (Disjoint Set)", "07_graphs/kruskals_mst.py"),

    ("8. Hashing", "Hash Table with Separate Chaining", "08_hashing/hash_table_chaining.py"),
    ("8. Hashing", "Hash Table with Open Addressing (Linear, Quad, Double)", "08_hashing/hash_table_open_addressing.py"),

    ("9. Classic Algorithms", "0/1 Knapsack (DP) & Fractional Knapsack (Greedy)", "09_classic_algorithms/knapsack_01_and_fractional.py"),
    ("9. Classic Algorithms", "Longest Common Subsequence (LCS)", "09_classic_algorithms/longest_common_subsequence.py"),
    ("9. Classic Algorithms", "Matrix Chain Multiplication (MCM)", "09_classic_algorithms/matrix_chain_multiplication.py"),
    ("9. Classic Algorithms", "N-Queens Problem (Backtracking)", "09_classic_algorithms/n_queens_backtracking.py"),
    ("9. Classic Algorithms", "Huffman Coding (Greedy Compression)", "09_classic_algorithms/huffman_coding.py"),
]


def run_experiment(script_rel_path: str) -> bool:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_dir, script_rel_path)

    if not os.path.exists(script_path):
        print(f"Error: File not found: {script_path}")
        return False

    print("\n" + "=" * 70)
    print(f"  EXECUTING: {os.path.basename(script_path)}")
    print(f"  PATH:      {script_rel_path}")
    print("=" * 70 + "\n")

    result = subprocess.run([sys.executable, script_path])
    return result.returncode == 0


def run_all_tests() -> None:
    print("\n" + "=" * 70)
    print("      RUNNING COMPLETE COLLEGE DSA LAB AUTOMATED TEST SUITE")
    print("=" * 70)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    passed = 0
    failed = 0

    for idx, (cat, title, rel_path) in enumerate(EXPERIMENTS, 1):
        script_path = os.path.join(base_dir, rel_path)
        sys.stdout.write(f"[{idx:02d}/{len(EXPERIMENTS)}] Testing {title:<45} ... ")
        sys.stdout.flush()

        res = subprocess.run(
            [sys.executable, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if res.returncode == 0:
            print("PASS")
            passed += 1
        else:
            print("FAIL")
            print(f"    Error: {res.stderr.strip()[:200]}")
            failed += 1

    print("\n" + "=" * 70)
    print(f"TEST SUITE SUMMARY: {passed} PASSED | {failed} FAILED | TOTAL: {len(EXPERIMENTS)}")
    print("=" * 70 + "\n")


def display_menu() -> None:
    print("\n" + "=" * 75)
    print("          COLLEGE & UNIVERSITY DSA LAB EXPERIMENTS REPOSITORY")
    print("=" * 75)

    current_cat = ""
    for idx, (cat, title, _) in enumerate(EXPERIMENTS, 1):
        if cat != current_cat:
            current_cat = cat
            print(f"\n  --- {cat.upper()} ---")
        print(f"  [{idx:2d}] {title}")

    print("\n  [ A] Run All Experiments (Automated Test Suite)")
    print("  [ Q] Quit")
    print("=" * 75)


def main():
    while True:
        display_menu()
        choice = input("Enter option (1-43, A, or Q): ").strip().upper()

        if choice in ("Q", "QUIT", "EXIT"):
            print("Exiting DSA Lab Runner. Happy learning!")
            break
        elif choice == "A":
            run_all_tests()
        elif choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(EXPERIMENTS):
                _, _, rel_path = EXPERIMENTS[idx - 1]
                run_experiment(rel_path)
            else:
                print(f"Invalid option! Please enter a number between 1 and {len(EXPERIMENTS)}.")
        else:
            print("Unrecognized selection. Try again.")

        input("\nPress Enter to return to main menu...")


if __name__ == "__main__":
    main()
