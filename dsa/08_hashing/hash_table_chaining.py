"""
Experiment: Hash Table with Separate Chaining
----------------------------------------------
Aim:
    To implement a Hash Table Abstract Data Type using Separate Chaining
    collision resolution, compute hash indices, support key-value pairs,
    and monitor the load factor.

Theory:
    In Separate Chaining, each slot of the hash table is a bucket (linked list
    or dynamic array). When two keys hash to the same bucket index (collision),
    the new key-value pair is simply appended to that bucket's list.

Load Factor:
    alpha = n / m
    where n = number of stored keys, m = number of buckets.
    When alpha exceeds a threshold (e.g. 0.75), rehashing to a larger prime
    capacity maintains O(1) average lookup time.

Time Complexity:
    - Insert:  O(1) average, O(n) worst case
    - Search:  O(1 + alpha) average, O(n) worst case
    - Delete:  O(1 + alpha) average, O(n) worst case

Space Complexity:
    - O(m + n)
"""

from typing import Any, List, Optional, Tuple


class HashNode:
    def __init__(self, key: Any, value: Any):
        self.key: Any = key
        self.value: Any = value
        self.next: Optional["HashNode"] = None

    def __repr__(self):
        return f"({self.key}: {self.value})"


class HashTableSeparateChaining:
    def __init__(self, capacity: int = 7):
        self.capacity: int = capacity
        self.size: int = 0
        self.buckets: List[Optional[HashNode]] = [None] * capacity

    def _hash(self, key: Any) -> int:
        """Computes hash index within bucket bounds."""
        return hash(key) % self.capacity

    def load_factor(self) -> float:
        return self.size / self.capacity

    def insert(self, key: Any, value: Any) -> None:
        """Inserts or updates a key-value pair."""
        index = self._hash(key)
        head = self.buckets[index]

        # Check if key already exists, update value
        curr = head
        while curr:
            if curr.key == key:
                curr.value = value
                return
            curr = curr.next

        # Insert new node at head of chain
        new_node = HashNode(key, value)
        new_node.next = self.buckets[index]
        self.buckets[index] = new_node
        self.size += 1

        # Check for rehash if load factor exceeds 0.75
        if self.load_factor() > 0.75:
            self._rehash()

    def get(self, key: Any) -> Any:
        """Retrieves value associated with key. Raises KeyError if absent."""
        index = self._hash(key)
        curr = self.buckets[index]
        while curr:
            if curr.key == key:
                return curr.value
            curr = curr.next
        raise KeyError(f"Key '{key}' not found in hash table.")

    def delete(self, key: Any) -> Any:
        """Deletes key-value pair and returns its value."""
        index = self._hash(key)
        curr = self.buckets[index]
        prev = None

        while curr:
            if curr.key == key:
                if prev is None:
                    self.buckets[index] = curr.next
                else:
                    prev.next = curr.next
                self.size -= 1
                return curr.value
            prev = curr
            curr = curr.next

        raise KeyError(f"Key '{key}' not found to delete.")

    def _rehash(self) -> None:
        """Doubles capacity and re-inserts all existing keys."""
        old_buckets = self.buckets
        self.capacity = self.capacity * 2 + 1  # Often chosen odd/prime
        self.buckets = [None] * self.capacity
        self.size = 0

        for head in old_buckets:
            curr = head
            while curr:
                self.insert(curr.key, curr.value)
                curr = curr.next

    def display(self) -> None:
        """Displays internal buckets and linked chains."""
        print(f"\nHash Table (Size: {self.size}, Capacity: {self.capacity}, Load Factor: {self.load_factor():.2f}):")
        for i in range(self.capacity):
            chain = []
            curr = self.buckets[i]
            while curr:
                chain.append(f"[{curr.key}: {curr.value}]")
                curr = curr.next
            chain_str = " -> ".join(chain) if chain else "Empty"
            print(f"  Bucket [{i:2d}]: {chain_str}")


if __name__ == "__main__":
    print("=" * 65)
    print("     COLLEGE DSA LAB: HASH TABLE (SEPARATE CHAINING)")
    print("=" * 65)

    ht = HashTableSeparateChaining(capacity=5)
    records = [
        ("Roll101", "Alice"),
        ("Roll102", "Bob"),
        ("Roll103", "Charlie"),
        ("Roll108", "David"),  # Causes deliberate collision
        ("Roll113", "Eve")     # Causes another collision
    ]

    for k, v in records:
        ht.insert(k, v)
        print(f"Inserted ({k}, {v})")

    ht.display()

    print(f"\nLookup 'Roll103': {ht.get('Roll103')}")
    print(f"Deleting 'Roll102': {ht.delete('Roll102')}")
    ht.display()
