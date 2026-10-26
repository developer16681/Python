"""
Experiment: Graph Representations (Adjacency Matrix & Adjacency List)
----------------------------------------------------------------------
Aim:
    To implement and compare the two fundamental graph representations:
    Adjacency Matrix and Adjacency List for both directed and undirected graphs.

Theory:
    1. Adjacency Matrix:
       A 2D array of size V x V where matrix[i][j] = 1 (or weight) if an edge
       exists from node i to node j, otherwise 0.
       - Space Complexity: O(V^2) (optimal for dense graphs).
       - Edge Lookup Time: O(1).
       - Finding all neighbors: O(V).

    2. Adjacency List:
       An array or hash map of lists where list[i] contains all adjacent vertices.
       - Space Complexity: O(V + E) (optimal for sparse graphs).
       - Edge Lookup Time: O(degree(u)).
       - Finding all neighbors: O(degree(u)).
"""

from typing import Dict, List, Tuple


class GraphAdjacencyMatrix:
    """
    Graph representation using a 2D V x V matrix.
    """
    def __init__(self, num_vertices: int, directed: bool = False):
        self.num_vertices = num_vertices
        self.directed = directed
        self.matrix: List[List[int]] = [[0] * num_vertices for _ in range(num_vertices)]

    def add_edge(self, u: int, v: int, weight: int = 1) -> None:
        if 0 <= u < self.num_vertices and 0 <= v < self.num_vertices:
            self.matrix[u][v] = weight
            if not self.directed:
                self.matrix[v][u] = weight
        else:
            raise IndexError("Vertex index out of bounds.")

    def has_edge(self, u: int, v: int) -> bool:
        return self.matrix[u][v] != 0

    def display(self) -> None:
        print("Adjacency Matrix:")
        header = "    " + " ".join(f"{i:3}" for i in range(self.num_vertices))
        print(header)
        print("   " + "-" * (4 * self.num_vertices))
        for i, row in enumerate(self.matrix):
            row_str = " ".join(f"{val:3}" for val in row)
            print(f"{i:2} | {row_str}")


class GraphAdjacencyList:
    """
    Graph representation using dictionary of lists/tuples.
    """
    def __init__(self, directed: bool = False):
        self.directed = directed
        self.adj: Dict[int, List[Tuple[int, int]]] = {}

    def add_vertex(self, u: int) -> None:
        if u not in self.adj:
            self.adj[u] = []

    def add_edge(self, u: int, v: int, weight: int = 1) -> None:
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))

    def get_neighbors(self, u: int) -> List[Tuple[int, int]]:
        return self.adj.get(u, [])

    def display(self) -> None:
        print("Adjacency List:")
        for vertex in sorted(self.adj.keys()):
            neighbors_str = ", ".join(f"({v}, wt={w})" for v, w in self.adj[vertex])
            print(f"  Node {vertex}: [{neighbors_str}]")


if __name__ == "__main__":
    print("=" * 65)
    print("      COLLEGE DSA LAB: GRAPH REPRESENTATIONS")
    print("=" * 65)

    edges = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 4), (3, 4, 2)]

    # 1. Adjacency Matrix
    print("--- 1. Undirected Graph using Adjacency Matrix ---")
    adj_mat = GraphAdjacencyMatrix(num_vertices=5, directed=False)
    for u, v, w in edges:
        adj_mat.add_edge(u, v, w)
    adj_mat.display()

    # 2. Adjacency List
    print("\n--- 2. Undirected Graph using Adjacency List ---")
    adj_list = GraphAdjacencyList(directed=False)
    for u, v, w in edges:
        adj_list.add_edge(u, v, w)
    adj_list.display()
