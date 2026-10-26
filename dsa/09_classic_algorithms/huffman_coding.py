"""
Experiment: Huffman Coding (Greedy Compression Algorithm)
----------------------------------------------------------
Aim:
    To implement Huffman Coding in Python using a Min-Priority Queue (Heap)
    to generate variable-length prefix-free binary codes based on character
    frequencies, and demonstrate message encoding and decoding.

Theory:
    Huffman Coding is a lossless data compression algorithm. It assigns
    variable-length codes to input characters based on their frequencies:
    - Highly frequent characters are assigned shorter bit sequences.
    - Less frequent characters are assigned longer bit sequences.
    - Prefix Rule: No code is a prefix of any other code, ensuring unambiguous decoding.

Algorithm:
    1. Count frequencies of each character.
    2. Insert all characters as leaf nodes into a Min-Heap keyed on frequency.
    3. While heap has more than one node:
       - Extract two minimum nodes (n1, n2).
       - Create new internal node with freq = n1.freq + n2.freq, left=n1, right=n2.
       - Re-insert new node into min-heap.
    4. The remaining node is the root of the Huffman Tree.
    5. Traverse tree: left branch appends '0', right branch appends '1'.

Time Complexity:
    - O(n log n) where n is number of unique characters.
Space Complexity:
    - O(n) for the binary tree and code table.
"""

from collections import Counter
import heapq
from typing import Dict, Optional, Tuple


class HuffmanNode:
    def __init__(self, char: Optional[str], freq: int):
        self.char: Optional[str] = char
        self.freq: int = freq
        self.left: Optional["HuffmanNode"] = None
        self.right: Optional["HuffmanNode"] = None

    def __lt__(self, other: "HuffmanNode") -> bool:
        return self.freq < other.freq

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


def build_huffman_tree(text: str) -> Optional[HuffmanNode]:
    """Builds Huffman Tree using character frequency min-heap."""
    if not text:
        return None

    freq_map = Counter(text)
    heap = [HuffmanNode(char, freq) for char, freq in freq_map.items()]
    heapq.heapify(heap)

    # Edge case: only one distinct character
    if len(heap) == 1:
        root = HuffmanNode(None, heap[0].freq)
        root.left = heap[0]
        return root

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        parent = HuffmanNode(None, left.freq + right.freq)
        parent.left = left
        parent.right = right
        heapq.heappush(heap, parent)

    return heap[0]


def generate_codes(root: Optional[HuffmanNode]) -> Dict[str, str]:
    """Generates binary prefix codes by traversing the Huffman Tree."""
    codes: Dict[str, str] = {}

    def _traverse(node: Optional[HuffmanNode], current_code: str):
        if not node:
            return
        if node.is_leaf() and node.char is not None:
            codes[node.char] = current_code or "0"
            return
        _traverse(node.left, current_code + "0")
        _traverse(node.right, current_code + "1")

    _traverse(root, "")
    return codes


def encode_text(text: str, codes: Dict[str, str]) -> str:
    """Encodes plaintext into a string of 0s and 1s."""
    return "".join(codes[ch] for ch in text)


def decode_text(encoded_str: str, root: Optional[HuffmanNode]) -> str:
    """Decodes a bitstring back into plaintext using the Huffman Tree."""
    if not root or not encoded_str:
        return ""

    decoded = []
    curr = root
    for bit in encoded_str:
        curr = curr.left if bit == "0" else curr.right
        assert curr is not None
        if curr.is_leaf():
            decoded.append(curr.char)  # type: ignore
            curr = root

    return "".join(decoded)


if __name__ == "__main__":
    print("=" * 65)
    print("        COLLEGE DSA LAB: HUFFMAN CODING")
    print("=" * 65)

    sample_text = "BEEP BOOP BEER!"
    print(f"Original Text: '{sample_text}' ({len(sample_text) * 8} bits in ASCII standard)\n")

    tree_root = build_huffman_tree(sample_text)
    huffman_codes = generate_codes(tree_root)

    print(f"{'Character':<12}{'Frequency':<12}{'Huffman Code'}")
    print("-" * 40)
    char_freqs = Counter(sample_text)
    for ch, freq in sorted(char_freqs.items(), key=lambda x: -x[1]):
        char_display = repr(ch)
        print(f"{char_display:<12}{freq:<12}{huffman_codes[ch]}")

    encoded = encode_text(sample_text, huffman_codes)
    decoded = decode_text(encoded, tree_root)

    print("-" * 40)
    print(f"Encoded Bitstring:  {encoded}")
    print(f"Compressed Length:  {len(encoded)} bits")
    print(f"Compression Ratio:  {(1 - len(encoded) / (len(sample_text) * 8)) * 100:.2f}% space saved")
    print(f"Decoded Message:    '{decoded}'")
    print(f"Integrity Check:    {'PASSED' if decoded == sample_text else 'FAILED'}")
