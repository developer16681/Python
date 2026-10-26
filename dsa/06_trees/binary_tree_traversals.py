"""
Experiment: Binary Tree Traversals (Recursive & Iterative) & Properties
-----------------------------------------------------------------------
Aim:
    To construct a Binary Tree in Python and implement Preorder, Inorder,
    Postorder (both recursive and iterative), and Level Order (Breadth-First)
    traversals, alongside calculating tree height, total node count, and leaf count.

Theory:
    A Binary Tree is a hierarchical non-linear data structure where each node
    has at most two children referred to as the left child and right child.

Depth-First Traversals:
    1. Inorder   (Left -> Root -> Right): Used in BST to retrieve sorted keys.
    2. Preorder  (Root -> Left -> Right): Used for tree duplication and prefix expressions.
    3. Postorder (Left -> Right -> Root): Used for tree deletion and postfix expressions.

Breadth-First Traversal:
    - Level Order Traversal: Visits nodes level by level from top to bottom,
      left to right using a FIFO queue.

Time Complexity:
    - All traversals: O(n) visiting each node exactly once.
Space Complexity:
    - Recursive DFS: O(h) where h is tree height (call stack).
    - Level Order:   O(w) where w is maximum width of the tree.
"""

from collections import deque
from typing import Any, List, Optional


class TreeNode:
    """Represents a node in a binary tree."""
    def __init__(self, data: Any):
        self.data: Any = data
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None

    def __repr__(self):
        return f"TreeNode({self.data})"


# 1. Recursive Traversals
def inorder_recursive(root: Optional[TreeNode]) -> List[Any]:
    if not root:
        return []
    return inorder_recursive(root.left) + [root.data] + inorder_recursive(root.right)


def preorder_recursive(root: Optional[TreeNode]) -> List[Any]:
    if not root:
        return []
    return [root.data] + preorder_recursive(root.left) + preorder_recursive(root.right)


def postorder_recursive(root: Optional[TreeNode]) -> List[Any]:
    if not root:
        return []
    return postorder_recursive(root.left) + postorder_recursive(root.right) + [root.data]


# 2. Iterative Traversals (Frequently tested in University Exams)
def inorder_iterative(root: Optional[TreeNode]) -> List[Any]:
    """Inorder traversal using explicit stack (Left -> Root -> Right)."""
    res = []
    stack = []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        res.append(curr.data)
        curr = curr.right
    return res


def preorder_iterative(root: Optional[TreeNode]) -> List[Any]:
    """Preorder traversal using explicit stack (Root -> Left -> Right)."""
    if not root:
        return []
    res = []
    stack = [root]
    while stack:
        node = stack.pop()
        res.append(node.data)
        # Push right first so that left is popped first
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return res


def postorder_iterative(root: Optional[TreeNode]) -> List[Any]:
    """Postorder traversal using two stacks or reverse preorder (Left -> Right -> Root)."""
    if not root:
        return []
    s1 = [root]
    s2 = []
    while s1:
        node = s1.pop()
        s2.append(node.data)
        if node.left:
            s1.append(node.left)
        if node.right:
            s1.append(node.right)
    return s2[::-1]


# 3. Breadth-First / Level Order Traversal
def level_order_traversal(root: Optional[TreeNode]) -> List[List[Any]]:
    """Returns level-by-level list of node values."""
    if not root:
        return []
    levels = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        current_level = []
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.data)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        levels.append(current_level)
    return levels


# 4. Tree Metrics
def tree_height(root: Optional[TreeNode]) -> int:
    """Calculates height of the tree (empty tree has height 0)."""
    if not root:
        return 0
    return 1 + max(tree_height(root.left), tree_height(root.right))


def count_nodes(root: Optional[TreeNode]) -> int:
    """Calculates total number of nodes in binary tree."""
    if not root:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)


def count_leaf_nodes(root: Optional[TreeNode]) -> int:
    """Calculates count of leaf nodes (nodes with 0 children)."""
    if not root:
        return 0
    if root.left is None and root.right is None:
        return 1
    return count_leaf_nodes(root.left) + count_leaf_nodes(root.right)


if __name__ == "__main__":
    print("=" * 65)
    print("      COLLEGE DSA LAB: BINARY TREE TRAVERSALS & METRICS")
    print("=" * 65)

    # Construct Sample Tree:
    #         1
    #       /   \
    #      2     3
    #     / \   / \
    #    4   5 6   7
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)

    print("Tree Structure:")
    print("        1        ")
    print("      /   \\      ")
    print("     2     3     ")
    print("    / \\   / \\    ")
    print("   4   5 6   7   \n")

    print(f"Preorder  (Recursive): {preorder_recursive(root)}")
    print(f"Preorder  (Iterative): {preorder_iterative(root)}")
    print(f"Inorder   (Recursive): {inorder_recursive(root)}")
    print(f"Inorder   (Iterative): {inorder_iterative(root)}")
    print(f"Postorder (Recursive): {postorder_recursive(root)}")
    print(f"Postorder (Iterative): {postorder_iterative(root)}")

    print(f"\nLevel Order Traversal: {level_order_traversal(root)}")
    print(f"Tree Height:           {tree_height(root)}")
    print(f"Total Nodes:           {count_nodes(root)}")
    print(f"Leaf Nodes Count:      {count_leaf_nodes(root)}")
