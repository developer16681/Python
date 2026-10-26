"""
Experiment: Balanced Parentheses / Delimiter Checker
------------------------------------------------------
Aim:
    To implement a syntax bracket validator using a Stack to check whether
    parentheses, curly braces, and square brackets are balanced and properly nested.

Theory:
    A string containing brackets `(`, `)`, `{`, `}`, `[`, `]` is valid if:
    1. Open brackets must be closed by the same type of brackets.
    2. Open brackets must be closed in the correct order.
    3. Every close bracket has a corresponding open bracket of the same type.

Algorithm:
    1. Initialize an empty stack.
    2. Scan each character of the string:
       - If opening bracket `(`, `{`, `[`, push to stack.
       - If closing bracket `)`, `}`, `]`:
         - If stack is empty, return False (unmatched closing bracket).
         - Pop top of stack. If it does not match the current closing bracket,
           return False (mismatched bracket types).
    3. At the end, return True if stack is empty, else False (unclosed brackets).

Time Complexity:
    - O(n) where n is length of expression.
Space Complexity:
    - O(n) for stack in worst case.
"""

from typing import Tuple


def is_balanced(expression: str) -> Tuple[bool, str]:
    """
    Checks if delimiters in the given expression are properly matched and balanced.
    
    Returns:
        A tuple of (is_valid: bool, reason: str).
    """
    bracket_map = {")": "(", "}": "{", "]": "["}
    stack = []

    for index, ch in enumerate(expression):
        if ch in bracket_map.values():
            stack.append((ch, index))
        elif ch in bracket_map.keys():
            if not stack:
                return False, f"Unmatched closing bracket '{ch}' at index {index}"
            top_char, top_idx = stack.pop()
            if top_char != bracket_map[ch]:
                return False, f"Mismatched '{top_char}' at {top_idx} closed by '{ch}' at {index}"

    if stack:
        top_char, top_idx = stack[-1]
        return False, f"Unclosed opening bracket '{top_char}' at index {top_idx}"

    return True, "Expression is completely balanced"


if __name__ == "__main__":
    print("=" * 65)
    print("      COLLEGE DSA LAB: BALANCED PARENTHESES CHECKER")
    print("=" * 65)

    test_cases = [
        "{ [ ( ) ] }",
        "((A + B) * [C - {D / E}])",
        "[(])",
        "{[()]}()",
        "((())",
        ")()(",
        "a + {b * [c + (d * e)]}"
    ]

    for expr in test_cases:
        valid, msg = is_balanced(expr)
        status = "BALANCED" if valid else "UNBALANCED"
        print(f"Expr:   {expr:<30} -> [{status}] | {msg}")
