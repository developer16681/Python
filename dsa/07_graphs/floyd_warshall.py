"""
Experiment: Floyd-Warshall All-Pairs Shortest Path Algorithm
------------------------------------------------------------
Aim:
    To implement the Floyd-Warshall dynamic programming algorithm in Python to
    compute shortest distances between every pair of vertices in a directed weighted graph.

Theory:
    Floyd-Warshall computes shortest paths between all pairs of vertices in O(V^3) time.
    It considers each vertex k as an intermediate vertex and updates:
        dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

Time Complexity:
    - O(V^3) with three nested loops.
Space Complexity:
    - O(V^2) for distance matrix.
"""

from typing import List


INF = float("inf")


def floyd_warshall(graph: List[List[float]]) -> List[List[float]]:
    """
    Computes all-pairs shortest distances matrix using Floyd-Warshall algorithm.
    """
    V = len(graph)
    # Initialize dist matrix as a copy of input graph
    dist = [row.copy() for row in graph]

    # k is the intermediate vertex
    for k in range(V):
        for i in range(V):
            for j in range(V):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist


def print_matrix(matrix: List[List[float]]) -> None:
    V = len(matrix)
    header = "      " + " ".join(f"[{j}]" for j in range(V))
    print(header)
    print("   " + "-" * (5 * V + 4))
    for i in range(V):
        row_str = " ".join(f"{matrix[i][j]:>4}" if matrix[i][j] != INF else " INF" for j in range(V))
        print(f"[{i}] | {row_str}")


if __name__ == "__main__":
    print("=" * 65)
    print("        COLLEGE DSA LAB: FLOYD-WARSHALL ALGORITHM")
    print("=" * 65)

    # 4-vertex weighted graph
    # 0 -> 1 (3), 0 -> 3 (7), 1 -> 0 (8), 1 -> 2 (2), 2 -> 0 (5), 2 -> 3 (1), 3 -> 0 (2)
    sample_graph = [
        [0,   3,   INF, 7],
        [8,   0,   2,   INF],
        [5,   INF, 0,   1],
        [2,   INF, INF, 0]
    ]

    print("Initial Cost Adjacency Matrix:")
    print_matrix(sample_graph)

    shortest_matrix = floyd_warshall(sample_graph)

    print("\nAll-Pairs Shortest Path Distance Matrix:")
    print_matrix(shortest_matrix)
