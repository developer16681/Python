r"""
Experiment: AVL Tree (Self-Balancing Binary Search Tree)
---------------------------------------------------------
Aim:
    To implement an AVL Tree in Python with automatic rebalancing through
    rotations (LL, RR, LR, RL), maintaining O(log n) worst-case time complexity.

Theory:
    An AVL tree is a self-balancing Binary Search Tree (BST) where the difference
    between heights of left and right subtrees (Balance Factor) cannot be more
    than 1 for all nodes:
        Balance Factor = height(left_subtree) - height(right_subtree)
        Valid Balance Factor in AVL: {-1, 0, +1}

Four Rotation Cases for Rebalancing:
    1. Left-Left (LL) Case: Right rotation at root.
    2. Right-Right (RR) Case: Left rotation at root.
    3. Left-Right (LR) Case: Left rotation on left child, then Right rotation at root.
    4. Right-Left (RL) Case: Right rotation on right child, then Left rotation at root.

Time Complexity:
    - Search, Insert, Delete: Strictly O(log n) in all cases (Worst, Average, Best).
Space Complexity:
    - O(n) storage with O(log n) recursion stack.
"""

from typing import List, Optional


class AVLNode:
    def __init__(self, key: int):
        self.key: int = key
        self.left: Optional["AVLNode"] = None
        self.right: Optional["AVLNode"] = None
        self.height: int = 1

    def __repr__(self):
        return f"AVLNode({self.key}, h={self.height})"


class AVLTree:
    def __init__(self):
        self.root: Optional[AVLNode] = None

    def get_height(self, node: Optional[AVLNode]) -> int:
        if not node:
            return 0
        return node.height

    def get_balance(self, node: Optional[AVLNode]) -> int:
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, y: AVLNode) -> AVLNode:
        r"""
        Right Rotation (Clockwise) on node y:
             y                x
            / \             /   \
           x   T3   -->    T1    y
          / \                   / \
         T1  T2                T2  T3
        """
        x = y.left
        assert x is not None
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        return x

    def left_rotate(self, x: AVLNode) -> AVLNode:
        r"""
        Left Rotation (Counter-Clockwise) on node x:
             x                 y
            / \              /   \
           T1  y    -->     x     T3
              / \          / \
             T2  T3       T1  T2
        """
        y = x.right
        assert y is not None
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def insert(self, key: int) -> None:
        """Public insert method."""
        self.root = self._insert_node(self.root, key)

    def _insert_node(self, node: Optional[AVLNode], key: int) -> AVLNode:
        # Step 1: Standard BST insert
        if not node:
            return AVLNode(key)

        if key < node.key:
            node.left = self._insert_node(node.left, key)
        elif key > node.key:
            node.right = self._insert_node(node.right, key)
        else:
            return node  # Duplicate keys not allowed

        # Step 2: Update height of this ancestor node
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # Step 3: Get balance factor to check whether this node became unbalanced
        balance = self.get_balance(node)

        # 4 Rotation Cases:

        # Case 1 - Left Left (LL)
        if balance > 1 and key < node.left.key:
            print(f"  [Rebalance] LL Rotation triggered at node {node.key}")
            return self.right_rotate(node)

        # Case 2 - Right Right (RR)
        if balance < -1 and key > node.right.key:
            print(f"  [Rebalance] RR Rotation triggered at node {node.key}")
            return self.left_rotate(node)

        # Case 3 - Left Right (LR)
        if balance > 1 and key > node.left.key:
            print(f"  [Rebalance] LR Rotation triggered at node {node.key}")
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Case 4 - Right Left (RL)
        if balance < -1 and key < node.right.key:
            print(f"  [Rebalance] RL Rotation triggered at node {node.key}")
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def inorder(self) -> List[int]:
        res = []
        def _inorder(node: Optional[AVLNode]):
            if node:
                _inorder(node.left)
                res.append(node.key)
                _inorder(node.right)
        _inorder(self.root)
        return res

    def print_tree(self, node: Optional[AVLNode] = None, prefix: str = "", is_left: bool = True) -> None:
        """ASCII Tree visualizer showing (key, BF=balance_factor, h=height)."""
        curr = node if node is not None else self.root
        if curr is None:
            return

        if curr.right:
            self.print_tree(curr.right, prefix + ("|   " if is_left else "    "), False)

        bf = self.get_balance(curr)
        print(prefix + ("+-- " if is_left else "+-- ") + f"{curr.key} (BF={bf}, h={curr.height})")

        if curr.left:
            self.print_tree(curr.left, prefix + ("    " if is_left else "|   "), True)


if __name__ == "__main__":
    print("=" * 65)
    print("        COLLEGE DSA LAB: AVL TREE (SELF-BALANCING)")
    print("=" * 65)

    avl = AVLTree()

    # Inserting strictly increasing sequence 10, 20, 30, 40, 50, 25
    # (In an ordinary BST, this would degenerate to an O(n) linked list!)
    keys_to_insert = [10, 20, 30, 40, 50, 25]

    for k in keys_to_insert:
        print(f"\nInserting {k}:")
        avl.insert(k)

    print("\nFinal Balanced AVL Tree Structure:")
    avl.print_tree()

    print(f"\nInorder Traversal: {avl.inorder()}")
    print(f"Root of balanced tree: {avl.root.key} (Height={avl.root.height})")
