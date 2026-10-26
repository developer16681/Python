"""
Experiment: Dijkstra's Single-Source Shortest Path Algorithm
-------------------------------------------------------------
Aim:
    To implement Dijkstra's algorithm using a Min-Heap (priority queue) to find
    the shortest path from a starting source vertex to all other vertices in a
    weighted graph with non-negative edge weights.

Theory:
    Dijkstra's algorithm is a greedy algorithm that determines the shortest
    path from a single source vertex to all other vertices in a weighted graph.
    It maintains a set of visited vertices and repeatedly selects the unvisited
    vertex with the minimal tentative distance.

Key Property:
    - Works only on graphs with NON-NEGATIVE edge weights.
    - If negative edges exist, Bellman-Ford algorithm must be used instead.

Time Complexity:
    - Using Min-Heap: O((V + E) log V)
Space Complexity:
    - O(V + E) for graph representation and distance array.
"""

import heapq
from typing import Dict, List, Optional, Tuple


class DijkstraGraph:
    def __init__(self, directed: bool = False):
        self.directed = directed
        self.adj: Dict[int, List[Tuple[int, float]]] = {}

    def add_edge(self, u: int, v: int, weight: float) -> None:
        if weight < 0:
            raise ValueError("Dijkstra does not support negative edge weights.")
        if u not in self.adj:
            self.adj[u] = []
        if v not in self.adj:
            self.adj[v] = []
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))

    def shortest_paths(self, start_vertex: int) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
        """
        Calculates shortest distance and predecessor mapping from start_vertex.
        """
        distances: Dict[int, float] = {v: float("inf") for v in self.adj}
        predecessors: Dict[int, Optional[int]] = {v: None for v in self.adj}
        distances[start_vertex] = 0.0

        # Min-Heap stores tuples of (distance, vertex)
        pq: List[Tuple[float, int]] = [(0.0, start_vertex)]

        while pq:
            current_dist, u = heapq.heappop(pq)

            # Skip if we found a shorter path to u already
            if current_dist > distances[u]:
                continue

            for neighbor, weight in self.adj[u]:
                distance_through_u = current_dist + weight
                if distance_through_u < distances[neighbor]:
                    distances[neighbor] = distance_through_u
                    predecessors[neighbor] = u
                    heapq.heappush(pq, (distance_through_u, neighbor))

        return distances, predecessors

    def get_path(self, predecessors: Dict[int, Optional[int]], target: int) -> List[int]:
        """Reconstructs path from source to target using predecessor map."""
        path = []
        curr: Optional[int] = target
        while curr is not None:
            path.append(curr)
            curr = predecessors[curr]
        return path[::-1]


if __name__ == "__main__":
    print("=" * 65)
    print("        COLLEGE DSA LAB: DIJKSTRA'S SHORTEST PATH")
    print("=" * 65)

    g = DijkstraGraph(directed=False)
    # Graph edges: (u, v, weight)
    weighted_edges = [
        (0, 1, 4), (0, 7, 8),
        (1, 2, 8), (1, 7, 11),
        (2, 3, 7), (2, 8, 2), (2, 5, 4),
        (3, 4, 9), (3, 5, 14),
        (4, 5, 10),
        (5, 6, 2),
        (6, 7, 1), (6, 8, 6),
        (7, 8, 7)
    ]

    for u, v, w in weighted_edges:
        g.add_edge(u, v, w)

    source = 0
    distances, predecessors = g.shortest_paths(source)

    print(f"Shortest paths from Source Vertex [{source}]:\n")
    print(f"{'Vertex':<10}{'Shortest Distance':<20}{'Full Path'}")
    print("-" * 55)

    for vertex in sorted(distances.keys()):
        dist = distances[vertex]
        path = g.get_path(predecessors, vertex)
        path_str = " -> ".join(map(str, path))
        print(f"{vertex:<10}{dist:<20}{path_str}")
