"""
Experiment: Kruskal's Minimum Spanning Tree Algorithm (Disjoint Set Union)
--------------------------------------------------------------------------
Aim:
    To implement Kruskal's algorithm for finding the Minimum Spanning Tree (MST)
    of a weighted undirected graph using Disjoint Set Union (DSU / Union-Find)
    with path compression and union by rank.

Theory:
    Kruskal's is an edge-centric greedy algorithm:
    1. Sort all the edges in non-decreasing order of their weight.
    2. Pick the smallest edge. Check if it forms a cycle with the spanning tree
       formed so far using Union-Find.
    3. If no cycle is formed, include this edge. Else, discard it.
    4. Repeat step 2 until there are (V - 1) edges in the spanning tree.

Disjoint Set Union (DSU):
    - find(i): Finds representative root of set containing i with path compression.
    - union(i, j): Merges sets containing i and j by comparing tree ranks.
    Both operations run in practically O(alpha(V)) (inverse Ackermann) time.

Time Complexity:
    - O(E log E) or O(E log V) to sort the edges.
Space Complexity:
    - O(V + E) for DSU structures and edge lists.
"""

from typing import List, Tuple


class DisjointSet:
    """Disjoint Set (Union-Find) with Path Compression and Union by Rank."""
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, i: int) -> int:
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])  # Path compression
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        """Merges sets containing i and j. Returns False if already in the same set."""
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i == root_j:
            return False  # Cycle detected

        # Union by rank
        if self.rank[root_i] < self.rank[root_j]:
            self.parent[root_i] = root_j
        elif self.rank[root_i] > self.rank[root_j]:
            self.parent[root_j] = root_i
        else:
            self.parent[root_j] = root_i
            self.rank[root_i] += 1

        return True


class KruskalsGraph:
    def __init__(self, num_vertices: int):
        self.V = num_vertices
        self.edges: List[Tuple[int, int, int]] = []  # (u, v, weight)

    def add_edge(self, u: int, v: int, weight: int) -> None:
        self.edges.append((u, v, weight))

    def kruskal_mst(self) -> Tuple[List[Tuple[int, int, int]], int]:
        # Step 1: Sort edges in non-decreasing order of weight
        sorted_edges = sorted(self.edges, key=lambda edge: edge[2])

        dsu = DisjointSet(self.V)
        mst = []
        total_weight = 0

        for u, v, weight in sorted_edges:
            # Step 2: Check if adding edge creates cycle
            if dsu.union(u, v):
                mst.append((u, v, weight))
                total_weight += weight
                if len(mst) == self.V - 1:
                    break

        return mst, total_weight


if __name__ == "__main__":
    print("=" * 65)
    print("        COLLEGE DSA LAB: KRUSKAL'S MST (UNION-FIND)")
    print("=" * 65)

    g = KruskalsGraph(num_vertices=9)
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

    mst_edges, total_cost = g.kruskal_mst()

    print(f"Total Minimum Spanning Tree Weight: {total_cost}\n")
    print("Edges selected in MST:")
    print(f"{'Edge (u - v)':<18}{'Weight'}")
    print("-" * 30)
    for u, v, w in mst_edges:
        print(f"{f'{u} -- {v}':<18}{w}")
