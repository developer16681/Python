"""
Experiment: Graph Traversals (Breadth-First Search & Depth-First Search)
------------------------------------------------------------------------
Aim:
    To implement Breadth-First Search (BFS) and Depth-First Search (DFS)
    traversals for graphs in Python, trace visitation sequences, count
    connected components, and test for path existence.

Theory:
    1. Breadth-First Search (BFS):
       Traverses graph level by level using a FIFO Queue. It explores all neighbors
       at the present depth prior to moving on to nodes at the next depth level.
       Application: Finding the shortest path on unweighted graphs.
       Time: O(V + E), Space: O(V).

    2. Depth-First Search (DFS):
       Explores as far as possible along each branch before backtracking using
       a LIFO Stack (or recursion).
       Application: Cycle detection, topological sorting, connected components.
       Time: O(V + E), Space: O(V).
"""

from collections import deque
from typing import Dict, List, Set


class GraphTraversal:
    def __init__(self, directed: bool = False):
        self.directed = directed
        self.adj: Dict[int, List[int]] = {}

    def add_edge(self, u: int, v: int) -> None:
        if u not in self.adj:
            self.adj[u] = []
        if v not in self.adj:
            self.adj[v] = []
        self.adj[u].append(v)
        if not self.directed:
            self.adj[v].append(u)

    def bfs(self, start_vertex: int) -> List[int]:
        """Breadth-First Search starting from start_vertex."""
        if start_vertex not in self.adj:
            return []

        visited: Set[int] = set()
        queue = deque([start_vertex])
        visited.add(start_vertex)
        traversal_order = []

        while queue:
            node = queue.popleft()
            traversal_order.append(node)

            for neighbor in sorted(self.adj[node]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return traversal_order

    def dfs_recursive(self, start_vertex: int) -> List[int]:
        """Depth-First Search (Recursive)."""
        visited: Set[int] = set()
        traversal_order: List[int] = []

        def _dfs(u: int):
            visited.add(u)
            traversal_order.append(u)
            for v in sorted(self.adj.get(u, [])):
                if v not in visited:
                    _dfs(v)

        if start_vertex in self.adj:
            _dfs(start_vertex)
        return traversal_order

    def dfs_iterative(self, start_vertex: int) -> List[int]:
        """Depth-First Search (Iterative using explicit stack)."""
        if start_vertex not in self.adj:
            return []

        visited: Set[int] = set()
        stack = [start_vertex]
        traversal_order = []

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                traversal_order.append(node)
                # Push in reverse sorted order so smaller vertices are visited first
                for neighbor in sorted(self.adj[node], reverse=True):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return traversal_order

    def find_connected_components(self) -> List[List[int]]:
        """Finds all connected components in an undirected graph."""
        visited: Set[int] = set()
        components = []

        for vertex in sorted(self.adj.keys()):
            if vertex not in visited:
                comp = []
                queue = deque([vertex])
                visited.add(vertex)
                while queue:
                    u = queue.popleft()
                    comp.append(u)
                    for v in sorted(self.adj[u]):
                        if v not in visited:
                            visited.add(v)
                            queue.append(v)
                components.append(comp)

        return components


if __name__ == "__main__":
    print("=" * 65)
    print("        COLLEGE DSA LAB: BFS & DFS GRAPH TRAVERSALS")
    print("=" * 65)

    # Graph with 2 disconnected components: {0,1,2,3,4} and {5,6}
    g = GraphTraversal(directed=False)
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 4), (5, 6)]
    for u, v in edges:
        g.add_edge(u, v)

    print("Graph Edges:", edges)
    print(f"BFS from vertex 0:             {g.bfs(0)}")
    print(f"DFS Recursive from vertex 0:   {g.dfs_recursive(0)}")
    print(f"DFS Iterative from vertex 0:   {g.dfs_iterative(0)}")

    components = g.find_connected_components()
    print(f"\nConnected Components ({len(components)} total):")
    for i, c in enumerate(components, 1):
        print(f"  Component {i}: {c}")
