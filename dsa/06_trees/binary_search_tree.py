"""
Experiment: Binary Search Tree (BST) Operations
------------------------------------------------
Aim:
    To implement a Binary Search Tree (BST) in Python, supporting key insertion,
    searching, node deletion (handling all 3 cases: leaf node, 1 child, and
    2 children using inorder successor), finding min/max, and sorted traversal.

Theory:
    A Binary Search Tree satisfies the BST property:
    - The left subtree of a node contains only keys lesser than the node's key.
    - The right subtree of a node contains only keys greater than the node's key.
    - Both left and right subtrees must also be binary search trees.
    
    Deletion Cases:
    1. Node to be deleted is a leaf: Simply remove it.
    2. Node to be deleted has only one child: Replace node with its child.
    3. Node to be deleted has two children: Find its inorder successor
       (smallest in right subtree), copy successor's content to the node,
       and recursively delete the inorder successor.

Time Complexity:
    - Search / Insert / Delete:
        - Best/Average Case: O(log n)
        - Worst Case:        O(n) (Skewed tree)
"""

from typing import Any, List, Optional


class BSTNode:
    def __init__(self, key: int):
        self.key: int = key
        self.left: Optional["BSTNode"] = None
        self.right: Optional["BSTNode"] = None

    def __repr__(self):
        return f"BSTNode({self.key})"


class BinarySearchTree:
    def __init__(self):
        self.root: Optional[BSTNode] = None

    def insert(self, key: int) -> None:
        """Inserts a key into the BST."""
        def _insert(node: Optional[BSTNode], val: int) -> BSTNode:
            if node is None:
                return BSTNode(val)
            if val < node.key:
                node.left = _insert(node.left, val)
            elif val > node.key:
                node.right = _insert(node.right, val)
            # Duplicate keys are ignored in standard BST
            return node

        self.root = _insert(self.root, key)

    def search_recursive(self, key: int) -> Optional[BSTNode]:
        """Searches for key recursively."""
        def _search(node: Optional[BSTNode], val: int) -> Optional[BSTNode]:
            if node is None or node.key == val:
                return node
            if val < node.key:
                return _search(node.left, val)
            return _search(node.right, val)

        return _search(self.root, key)

    def search_iterative(self, key: int) -> Optional[BSTNode]:
        """Searches for key iteratively without call stack overhead."""
        curr = self.root
        while curr:
            if curr.key == key:
                return curr
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return None

    def find_min(self, node: Optional[BSTNode] = None) -> Optional[BSTNode]:
        """Returns the node with the minimum key."""
        curr = node if node else self.root
        if curr is None:
            return None
        while curr.left:
            curr = curr.left
        return curr

    def find_max(self, node: Optional[BSTNode] = None) -> Optional[BSTNode]:
        """Returns the node with the maximum key."""
        curr = node if node else self.root
        if curr is None:
            return None
        while curr.right:
            curr = curr.right
        return curr

    def delete(self, key: int) -> None:
        """Deletes a node by key from the BST."""
        def _delete(node: Optional[BSTNode], val: int) -> Optional[BSTNode]:
            if node is None:
                return None

            if val < node.key:
                node.left = _delete(node.left, val)
            elif val > node.key:
                node.right = _delete(node.right, val)
            else:
                # Case 1 & 2: Node with 0 or 1 child
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left

                # Case 3: Node with 2 children
                # Get the inorder successor (smallest in the right subtree)
                successor = self.find_min(node.right)
                assert successor is not None
                node.key = successor.key
                # Delete the inorder successor from right subtree
                node.right = _delete(node.right, successor.key)

            return node

        self.root = _delete(self.root, key)

    def inorder(self) -> List[int]:
        """Inorder traversal gives sorted keys."""
        res = []
        def _inorder(node: Optional[BSTNode]):
            if node:
                _inorder(node.left)
                res.append(node.key)
                _inorder(node.right)
        _inorder(self.root)
        return res

    def print_tree_structure(self, node: Optional[BSTNode] = None, prefix: str = "", is_left: bool = True) -> None:
        """Pretty prints tree structure visually in ASCII."""
        curr = node if node is not None else self.root
        if curr is None:
            print("(Tree is empty)")
            return

        if curr.right:
            self.print_tree_structure(curr.right, prefix + ("|   " if is_left else "    "), False)

        print(prefix + ("+-- " if is_left else "+-- ") + str(curr.key))

        if curr.left:
            self.print_tree_structure(curr.left, prefix + ("    " if is_left else "|   "), True)


if __name__ == "__main__":
    print("=" * 65)
    print("        COLLEGE DSA LAB: BINARY SEARCH TREE (BST)")
    print("=" * 65)

    bst = BinarySearchTree()
    keys = [50, 30, 70, 20, 40, 60, 80]
    print(f"Inserting keys: {keys}\n")
    for k in keys:
        bst.insert(k)

    print("Visual BST Structure:")
    bst.print_tree_structure()

    print(f"\nInorder Traversal (Sorted order): {bst.inorder()}")
    print(f"Minimum Key: {bst.find_min().key}")
    print(f"Maximum Key: {bst.find_max().key}")

    # Search
    for query in [40, 99]:
        found = bst.search_iterative(query)
        print(f"Search for {query}: {'Found' if found else 'Not Found'}")

    # Deletion Case 1: Leaf node (20)
    print("\n--- Deleting Leaf Node (20) ---")
    bst.delete(20)
    print(f"Inorder: {bst.inorder()}")

    # Deletion Case 2: Node with 1 child (30 now has only right child 40)
    print("\n--- Deleting Node with 1 Child (30) ---")
    bst.delete(30)
    print(f"Inorder: {bst.inorder()}")

    # Deletion Case 3: Root Node with 2 children (50)
    print("\n--- Deleting Root Node with 2 Children (50) ---")
    bst.delete(50)
    print(f"Inorder: {bst.inorder()}")
    print("\nUpdated Visual BST Structure:")
    bst.print_tree_structure()
