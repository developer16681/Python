"""
Experiment: Hash Table with Open Addressing (Linear, Quadratic, Double Hashing)
--------------------------------------------------------------------------------
Aim:
    To implement Open Addressing collision resolution strategies:
    1. Linear Probing:      h(k, i) = (h'(k) + i) mod m
    2. Quadratic Probing:   h(k, i) = (h'(k) + i^2) mod m
    3. Double Hashing:      h(k, i) = (h1(k) + i * h2(k)) mod m
    using tombstone markers (DELETED) for safe deletions.

Theory:
    In open addressing, all elements are stored directly in the hash table array.
    When a collision occurs, alternative cells are probed until an empty cell is found.
    - Tombstone Marker: When an element is deleted, the slot is marked as DELETED
      rather than EMPTY so that future search chains do not break prematurely.

Time Complexity:
    - Average: O(1) for insert, search, delete with load factor < 0.7.
    - Worst:   O(n) if severe clustering occurs.
"""

from typing import Any, List, Optional, Tuple


DELETED = object()  # Sentinel tombstone for deleted slots


class OpenAddressingHashTable:
    def __init__(self, capacity: int = 11, mode: str = "linear"):
        """
        mode: 'linear', 'quadratic', or 'double'
        """
        self.capacity = capacity
        self.mode = mode.lower()
        self.keys: List[Any] = [None] * capacity
        self.values: List[Any] = [None] * capacity
        self.size = 0

    def _h1(self, key: Any) -> int:
        return hash(key) % self.capacity

    def _h2(self, key: Any) -> int:
        # Must be non-zero and relatively prime to capacity
        return 7 - (hash(key) % 7)

    def _probe_index(self, key: Any, i: int) -> int:
        base = self._h1(key)
        if self.mode == "linear":
            return (base + i) % self.capacity
        elif self.mode == "quadratic":
            return (base + i * i) % self.capacity
        elif self.mode == "double":
            return (base + i * self._h2(key)) % self.capacity
        else:
            raise ValueError(f"Unknown mode: {self.mode}")

    def insert(self, key: Any, value: Any) -> None:
        if self.size >= self.capacity:
            raise OverflowError("Hash table is completely full.")

        first_deleted_slot = None

        for i in range(self.capacity):
            idx = self._probe_index(key, i)

            if self.keys[idx] == key:  # Key already exists: update value
                self.values[idx] = value
                return

            if self.keys[idx] is DELETED and first_deleted_slot is None:
                first_deleted_slot = idx

            if self.keys[idx] is None:
                # Use previously seen tombstone slot if available, else current slot
                target_idx = first_deleted_slot if first_deleted_slot is not None else idx
                self.keys[target_idx] = key
                self.values[target_idx] = value
                self.size += 1
                return

        if first_deleted_slot is not None:
            self.keys[first_deleted_slot] = key
            self.values[first_deleted_slot] = value
            self.size += 1
            return

        raise OverflowError("Could not find open slot due to probing cycle.")

    def search(self, key: Any) -> Optional[Any]:
        for i in range(self.capacity):
            idx = self._probe_index(key, i)
            if self.keys[idx] is None:
                return None  # Unoccupied slot terminates search
            if self.keys[idx] == key:
                return self.values[idx]
        return None

    def delete(self, key: Any) -> bool:
        for i in range(self.capacity):
            idx = self._probe_index(key, i)
            if self.keys[idx] is None:
                return False
            if self.keys[idx] == key:
                self.keys[idx] = DELETED
                self.values[idx] = None
                self.size -= 1
                return True
        return False

    def display(self) -> None:
        print(f"\nOpen Addressing Table (Mode: {self.mode.upper()}, Capacity: {self.capacity}):")
        for i in range(self.capacity):
            k = self.keys[i]
            if k is None:
                state = "<EMPTY>"
            elif k is DELETED:
                state = "<DELETED TOMBSTONE>"
            else:
                state = f"Key: {k}, Value: {self.values[i]}"
            print(f"  Slot [{i:2d}]: {state}")


if __name__ == "__main__":
    print("=" * 65)
    print("   COLLEGE DSA LAB: OPEN ADDRESSING (LINEAR, QUAD, DOUBLE)")
    print("=" * 65)

    keys_data = [(10, "Ten"), (21, "Twenty-One"), (32, "Thirty-Two"), (43, "Forty-Three")]

    for mode in ["linear", "quadratic", "double"]:
        table = OpenAddressingHashTable(capacity=11, mode=mode)
        print(f"\n--- Testing Mode: {mode.upper()} PROBING ---")
        for k, v in keys_data:
            table.insert(k, v)
        table.display()

        # Delete an element and verify search succeeds for subsequent probed element
        print(f"\nDeleting key 21...")
        table.delete(21)
        table.display()
        print(f"Lookup for key 32 (probed past tombstone): {table.search(32)}")
