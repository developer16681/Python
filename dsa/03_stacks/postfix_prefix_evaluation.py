"""
Experiment: Postfix and Prefix Expression Evaluation
------------------------------------------------------
Aim:
    To evaluate Postfix (Reverse Polish) and Prefix (Polish) arithmetic expressions
    using a Stack data structure in Python, handling multi-digit operands and
    standard arithmetic operators.

Theory:
    Evaluation of Postfix:
    1. Scan tokens from left to right.
    2. If token is an operand (number), push onto the stack.
    3. If token is an operator, pop two operands:
       op2 = pop()
       op1 = pop()
       result = op1 (operator) op2
       Push result back onto stack.
    4. At the end, the stack contains the final evaluated result.

    Evaluation of Prefix:
    1. Scan tokens from right to left.
    2. If token is an operand, push onto the stack.
    3. If token is an operator:
       op1 = pop()
       op2 = pop()
       result = op1 (operator) op2
       Push result back onto stack.
    4. At the end, the stack top is the final evaluated result.

Time Complexity:
    - O(n) where n is number of tokens.
Space Complexity:
    - O(n) auxiliary stack space.
"""

from typing import List, Union


def apply_op(op: str, val1: float, val2: float) -> float:
    """Computes arithmetic binary operation val1 op val2."""
    if op == "+":
        return val1 + val2
    elif op == "-":
        return val1 - val2
    elif op == "*":
        return val1 * val2
    elif op == "/":
        if val2 == 0:
            raise ZeroDivisionError("Division by zero in expression evaluation.")
        return val1 / val2
    elif op == "^":
        return val1 ** val2
    elif op == "%":
        return val1 % val2
    else:
        raise ValueError(f"Unknown operator: {op}")


def evaluate_postfix(expr: str) -> float:
    """
    Evaluates a postfix expression. Operands and operators can be space-separated
    or individual characters (e.g., '2 3 1 * + 9 -' or '231*+9-').
    """
    stack: List[float] = []
    # If expression contains spaces, split by whitespace; otherwise treat each char as token
    tokens = expr.split() if " " in expr.strip() else list(expr.strip())

    for token in tokens:
        if token in ("+", "-", "*", "/", "^", "%"):
            if len(stack) < 2:
                raise ValueError("Malformed postfix expression: insufficient operands.")
            op2 = stack.pop()
            op1 = stack.pop()
            res = apply_op(token, op1, op2)
            stack.append(res)
        else:
            try:
                stack.append(float(token))
            except ValueError:
                raise ValueError(f"Invalid operand token: '{token}'")

    if len(stack) != 1:
        raise ValueError("Malformed postfix expression: too many operands remaining.")
    return stack[0]


def evaluate_prefix(expr: str) -> float:
    """
    Evaluates a prefix expression scanning from right to left.
    """
    stack: List[float] = []
    tokens = expr.split() if " " in expr.strip() else list(expr.strip())

    # Traverse from right to left
    for token in reversed(tokens):
        if token in ("+", "-", "*", "/", "^", "%"):
            if len(stack) < 2:
                raise ValueError("Malformed prefix expression: insufficient operands.")
            op1 = stack.pop()
            op2 = stack.pop()
            res = apply_op(token, op1, op2)
            stack.append(res)
        else:
            try:
                stack.append(float(token))
            except ValueError:
                raise ValueError(f"Invalid operand token: '{token}'")

    if len(stack) != 1:
        raise ValueError("Malformed prefix expression: too many operands remaining.")
    return stack[0]


if __name__ == "__main__":
    print("=" * 65)
    print("     COLLEGE DSA LAB: POSTFIX & PREFIX EVALUATION")
    print("=" * 65)

    # 1. Postfix Evaluation
    postfix_examples = [
        ("2 3 1 * + 9 -", -4.0),
        ("100 200 + 2 / 5 * 7 +", 757.0),
        ("5 3 ^ 2 *", 250.0)
    ]

    print("--- Postfix Evaluation Results ---")
    for expr, expected in postfix_examples:
        result = evaluate_postfix(expr)
        print(f"Postfix Expr: {expr:<25} -> Result: {result} (Expected: {expected})")

    # 2. Prefix Evaluation
    prefix_examples = [
        ("+ 9 * 2 6", 21.0),
        ("- + 2 * 3 1 9", -4.0),
        ("* + 1 2 3", 9.0)
    ]

    print("\n--- Prefix Evaluation Results ---")
    for expr, expected in prefix_examples:
        result = evaluate_prefix(expr)
        print(f"Prefix Expr:  {expr:<25} -> Result: {result} (Expected: {expected})")
