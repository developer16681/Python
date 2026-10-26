"""
Experiment: Prim's Minimum Spanning Tree (MST) Algorithm
---------------------------------------------------------
Aim:
    To implement Prim's algorithm in Python using a priority queue (min-heap)
    to find the Minimum Spanning Tree of a connected, undirected, weighted graph.

Theory:
    A Minimum Spanning Tree (MST) of an undirected weighted graph is a subgraph
    that connects all vertices with V - 1 edges and minimum total edge weight,
    without containing any cycles.
    
    Prim's Algorithm (Greedy):
    - Starts with an arbitrary vertex in the MST set.
    - At each step, finds the minimum-weight edge connecting a vertex in the
      MST to a vertex outside the MST using a Min-Heap.
    - Adds the edge and vertex to the MST set until all V vertices are included.

Time Complexity:
    - O((V + E) log V) with Min-Heap / Priority Queue.
Space Complexity:
    - O(V + E) for adjacency list and priority queue.
"""

import heapq
from typing import Dict, List, Set, Tuple


class PrimsGraph:
    def __init__(self):
        self.adj: Dict[int, List[Tuple[int, int]]] = {}

    def add_edge(self, u: int, v: int, weight: int) -> None:
        if u not in self.adj:
            self.adj[u] = []
        if v not in self.adj:
            self.adj[v] = []
        self.adj[u].append((v, weight))
        self.adj[v].append((u, weight))

    def prim_mst(self, start_node: int = 0) -> Tuple[List[Tuple[int, int, int]], int]:
        """
        Executes Prim's algorithm.
        Returns:
            (mst_edges: List of (u, v, weight), total_mst_weight: int)
        """
        if not self.adj:
            return [], 0

        mst_edges: List[Tuple[int, int, int]] = []
        visited: Set[int] = set()
        total_weight = 0

        # Min-heap elements: (weight, current_node, parent_node)
        pq: List[Tuple[int, int, int]] = [(0, start_node, -1)]

        while pq and len(visited) < len(self.adj):
            weight, u, parent = heapq.heappop(pq)

            if u in visited:
                continue

            visited.add(u)
            if parent != -1:
                mst_edges.append((parent, u, weight))
                total_weight += weight

            for neighbor, edge_wt in self.adj[u]:
                if neighbor not in visited:
                    heapq.heappush(pq, (edge_wt, neighbor, u))

        return mst_edges, total_weight


if __name__ == "__main__":
    print("=" * 65)
    print("        COLLEGE DSA LAB: PRIM'S MINIMUM SPANNING TREE")
    print("=" * 65)

    g = PrimsGraph()
    # Graph edges: (u, v, weight)
    edges = [
        (0, 1, 4), (0, 7, 8),
        (1, 2, 8), (1, 7, 11),
        (2, 3, 7), (2, 8, 2), (2, 5, 4),
        (3, 4, 9), (3, 5, 14),
        (4, 5, 10),
        (5, 6, 2),
        (6, 7, 1), (6, 8, 6),
        (7, 8, 7)
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)

    mst, cost = g.prim_mst(start_node=0)

    print(f"Total Minimum Spanning Tree Weight: {cost}\n")
    print("Edges included in MST:")
    print(f"{'Edge (u - v)':<18}{'Weight'}")
    print("-" * 30)
    for u, v, w in mst:
        print(f"{f'{u} -- {v}':<18}{w}")
