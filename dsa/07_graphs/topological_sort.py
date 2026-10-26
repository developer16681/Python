"""
Experiment: Topological Sort (Kahn's Algorithm & DFS Based)
-----------------------------------------------------------
Aim:
    To implement Topological Sorting for Directed Acyclic Graphs (DAG) using:
    1. Kahn's Algorithm (BFS-based in-degree method)
    2. DFS-based Post-visit Stack method
    and detect cycles if present.

Theory:
    Topological ordering of a directed graph is a linear ordering of its vertices
    such that for every directed edge u -> v, vertex u comes before v in the ordering.
    A topological sort is possible if and only if the graph has no directed cycles (i.e. DAG).

Algorithms:
    1. Kahn's Algorithm:
       - Compute in-degree (number of incoming edges) for each vertex.
       - Enqueue vertices with in-degree 0.
       - Dequeue vertex, append to topological order, and decrement in-degree of its neighbors.
       - If a neighbor's in-degree becomes 0, enqueue it.
       - If processed nodes count != total nodes, graph contains a cycle!

    2. DFS-based:
       - Maintain visited states (0=unvisited, 1=visiting, 2=visited).
       - When visiting node finishes all child DFS branches, push it onto stack.
       - Pop all from stack to get topological order.

Time Complexity:
    - O(V + E) for both methods.
Space Complexity:
    - O(V) for in-degree array / call stack.
"""

from collections import deque
from typing import Dict, List, Optional


class DAG:
    def __init__(self):
        self.adj: Dict[int, List[int]] = {}

    def add_edge(self, u: int, v: int) -> None:
        if u not in self.adj:
            self.adj[u] = []
        if v not in self.adj:
            self.adj[v] = []
        self.adj[u].append(v)

    def topological_sort_kahns(self) -> Optional[List[int]]:
        """Kahn's Algorithm (BFS with in-degrees). Returns None if cycle exists."""
        in_degree = {v: 0 for v in self.adj}
        for u in self.adj:
            for v in self.adj[u]:
                in_degree[v] += 1

        queue = deque([v for v, deg in in_degree.items() if deg == 0])
        topo_order = []

        while queue:
            u = queue.popleft()
            topo_order.append(u)

            for v in self.adj[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        if len(topo_order) != len(self.adj):
            return None  # Cycle detected

        return topo_order

    def topological_sort_dfs(self) -> Optional[List[int]]:
        """DFS-based topological sort with 3-color cycle detection."""
        # state: 0 = unvisited, 1 = currently in recursion stack, 2 = fully visited
        state = {v: 0 for v in self.adj}
        stack = []
        has_cycle = False

        def _dfs(u: int):
            nonlocal has_cycle
            if has_cycle:
                return

            state[u] = 1  # visiting
            for v in self.adj[u]:
                if state[v] == 1:
                    has_cycle = True
                    return
                elif state[v] == 0:
                    _dfs(v)

            state[u] = 2  # finished
            stack.append(u)

        for vertex in sorted(self.adj.keys()):
            if state[vertex] == 0:
                _dfs(vertex)

        if has_cycle:
            return None

        return stack[::-1]


if __name__ == "__main__":
    print("=" * 65)
    print("        COLLEGE DSA LAB: TOPOLOGICAL SORT")
    print("=" * 65)

    dag = DAG()
    # Prerequisite course dependency graph:
    # 5 -> 2, 5 -> 0, 4 -> 0, 4 -> 1, 2 -> 3, 3 -> 1
    edges = [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]
    for u, v in edges:
        dag.add_edge(u, v)

    print(f"Directed Edges: {edges}")
    kahn_order = dag.topological_sort_kahns()
    dfs_order = dag.topological_sort_dfs()

    print(f"Topological Sort (Kahn's BFS):  {kahn_order}")
    print(f"Topological Sort (DFS Based):   {dfs_order}")

    # Cyclic graph test
    cyclic = DAG()
    for u, v in [(0, 1), (1, 2), (2, 0)]:
        cyclic.add_edge(u, v)

    print("\nTesting Cyclic Graph [(0->1), (1->2), (2->0)]:")
    print(f"Kahn's result (Cycle?): {cyclic.topological_sort_kahns() is None} (Returns None)")
