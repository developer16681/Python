"""
Experiment: Bellman-Ford Shortest Path Algorithm
-------------------------------------------------
Aim:
    To implement the Bellman-Ford algorithm in Python to find shortest paths
    from a single source, handle negative edge weights, and detect negative-weight
    cycles.

Theory:
    Unlike Dijkstra's algorithm, the Bellman-Ford algorithm works on graphs
    with negative edge weights. It uses dynamic programming and relaxes all
    edges |V| - 1 times.
    
    Negative Cycle Detection:
    If after |V| - 1 iterations of relaxation, any edge can still be relaxed,
    the graph contains a negative-weight cycle reachable from the source,
    meaning an infinitely small path distance is possible.

Time Complexity:
    - O(V * E)
Space Complexity:
    - O(V) for distances array.
"""

from typing import List, Optional, Tuple


class Edge:
    def __init__(self, u: int, v: int, weight: float):
        self.u = u
        self.v = v
        self.weight = weight


class BellmanFordGraph:
    def __init__(self, vertices_count: int):
        self.V = vertices_count
        self.edges: List[Edge] = []

    def add_edge(self, u: int, v: int, weight: float) -> None:
        self.edges.append(Edge(u, v, weight))

    def shortest_path(self, src: int) -> Tuple[Optional[List[float]], bool]:
        """
        Runs Bellman-Ford from src.
        Returns (distances, has_negative_cycle).
        If has_negative_cycle is True, distances may be invalid.
        """
        dist = [float("inf")] * self.V
        dist[src] = 0.0

        # Step 1: Relax all edges |V| - 1 times
        for _ in range(self.V - 1):
            updated = False
            for edge in self.edges:
                if dist[edge.u] != float("inf") and dist[edge.u] + edge.weight < dist[edge.v]:
                    dist[edge.v] = dist[edge.u] + edge.weight
                    updated = True
            if not updated:
                break  # Early exit if no relaxation occurred

        # Step 2: Check for negative-weight cycles
        for edge in self.edges:
            if dist[edge.u] != float("inf") and dist[edge.u] + edge.weight < dist[edge.v]:
                return None, True  # Negative cycle detected

        return dist, False


if __name__ == "__main__":
    print("=" * 65)
    print("        COLLEGE DSA LAB: BELLMAN-FORD ALGORITHM")
    print("=" * 65)

    # Graph 1: Standard graph with negative weights (No negative cycle)
    g1 = BellmanFordGraph(vertices_count=5)
    edges1 = [
        (0, 1, -1), (0, 2, 4),
        (1, 2, 3), (1, 3, 2), (1, 4, 2),
        (3, 2, 5), (3, 1, 1),
        (4, 3, -3)
    ]
    for u, v, w in edges1:
        g1.add_edge(u, v, w)

    distances, has_cycle = g1.shortest_path(src=0)
    print("Graph 1 (With negative weights, no negative cycle):")
    print(f"Negative Cycle Detected: {has_cycle}")
    for i, d in enumerate(distances):
        print(f"  Shortest distance from 0 to vertex {i}: {d}")

    # Graph 2: Graph with a negative-weight cycle (1 -> 2 -> 3 -> 1 with sum < 0)
    g2 = BellmanFordGraph(vertices_count=4)
    g2.add_edge(0, 1, 1)
    g2.add_edge(1, 2, 2)
    g2.add_edge(2, 3, -7)
    g2.add_edge(3, 1, 2)

    print("\nGraph 2 (Contains negative cycle 1 -> 2 -> 3 -> 1):")
    _, has_neg_cycle = g2.shortest_path(src=0)
    print(f"Negative Cycle Detected: {has_neg_cycle}")
