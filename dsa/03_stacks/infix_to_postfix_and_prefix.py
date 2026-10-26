"""
Experiment: Infix to Postfix and Prefix Conversion (Stack Application)
-----------------------------------------------------------------------
Aim:
    To implement algorithms to convert standard Infix arithmetic expressions
    into Postfix (Reverse Polish Notation) and Prefix (Polish Notation) forms
    using a Stack data structure with operator precedence and associativity rules.

Theory:
    - Infix: Operators are placed between operands (e.g. A + B).
    - Postfix: Operators are placed after operands (e.g. A B +).
    - Prefix: Operators are placed before operands (e.g. + A B).

Precedence Rules:
    ^ (Power): Precedence 3, Right-to-Left Associative
    *, /, %:   Precedence 2, Left-to-Right Associative
    +, -:      Precedence 1, Left-to-Right Associative

Algorithm for Infix to Postfix:
    1. Scan characters from left to right.
    2. If operand, add directly to output.
    3. If '(', push onto stack.
    4. If ')', pop until '(' is encountered.
    5. If operator, pop operators from stack having greater or equal precedence
       (strictly greater for right-associative '^'), then push current operator.
    6. Pop remaining operators from stack.

Algorithm for Infix to Prefix:
    1. Reverse the infix expression.
    2. Swap '(' with ')' and vice versa.
    3. Convert to postfix using the modified precedence rule.
    4. Reverse the resulting postfix expression to obtain prefix.

Time Complexity:
    - O(n) where n is length of expression.
Space Complexity:
    - O(n) auxiliary stack space.
"""

from typing import List, Tuple


def get_precedence(op: str) -> int:
    """Returns the precedence level of an arithmetic operator."""
    if op == "^":
        return 3
    if op in ("*", "/", "%"):
        return 2
    if op in ("+", "-"):
        return 1
    return 0


def is_right_associative(op: str) -> bool:
    """Returns True if the operator is right-associative."""
    return op == "^"


def infix_to_postfix(expr: str, trace: bool = False) -> str:
    """
    Converts an Infix arithmetic expression into Postfix notation.
    """
    stack: List[str] = []
    postfix: List[str] = []

    if trace:
        print(f"\nTracing Infix to Postfix for: '{expr}'")
        print(f"{'Char':<6}{'Action':<28}{'Stack':<18}{'Postfix Output'}")
        print("-" * 75)

    for ch in expr:
        if ch.isspace():
            continue

        if ch.isalnum():
            postfix.append(ch)
            if trace:
                print(f"{ch:<6}{'Append operand to output':<28}{''.join(stack):<18}{''.join(postfix)}")

        elif ch == "(":
            stack.append(ch)
            if trace:
                print(f"{ch:<6}{'Push ( to stack':<28}{''.join(stack):<18}{''.join(postfix)}")

        elif ch == ")":
            while stack and stack[-1] != "(":
                postfix.append(stack.pop())
            if stack and stack[-1] == "(":
                stack.pop()  # Discard '('
            if trace:
                print(f"{ch:<6}{'Pop stack until (':<28}{''.join(stack):<18}{''.join(postfix)}")

        else:  # Operator
            while stack and stack[-1] != "(" and (
                get_precedence(stack[-1]) > get_precedence(ch) or
                (get_precedence(stack[-1]) == get_precedence(ch) and not is_right_associative(ch))
            ):
                postfix.append(stack.pop())
            stack.append(ch)
            if trace:
                print(f"{ch:<6}{f'Push operator {ch}':<28}{''.join(stack):<18}{''.join(postfix)}")

    while stack:
        postfix.append(stack.pop())

    result = "".join(postfix)
    if trace:
        print("-" * 75)
        print(f"Final Postfix: {result}\n")

    return result


def infix_to_prefix(expr: str) -> str:
    """
    Converts an Infix arithmetic expression into Prefix notation.
    """
    # 1. Reverse the string
    rev = list(expr[::-1])

    # 2. Swap '(' and ')'
    for i, ch in enumerate(rev):
        if ch == "(":
            rev[i] = ")"
        elif ch == ")":
            rev[i] = "("

    reversed_expr = "".join(rev)

    # 3. Postfix conversion with right-associativity tweak
    stack: List[str] = []
    prefix: List[str] = []

    for ch in reversed_expr:
        if ch.isspace():
            continue

        if ch.isalnum():
            prefix.append(ch)
        elif ch == "(":
            stack.append(ch)
        elif ch == ")":
            while stack and stack[-1] != "(":
                prefix.append(stack.pop())
            if stack and stack[-1] == "(":
                stack.pop()
        else:
            while stack and stack[-1] != "(" and (
                get_precedence(stack[-1]) > get_precedence(ch) or
                (get_precedence(stack[-1]) == get_precedence(ch) and is_right_associative(ch))
            ):
                prefix.append(stack.pop())
            stack.append(ch)

    while stack:
        prefix.append(stack.pop())

    # 4. Reverse output to get Prefix
    return "".join(prefix[::-1])


if __name__ == "__main__":
    print("=" * 75)
    print("      COLLEGE DSA LAB: INFIX TO POSTFIX & PREFIX CONVERSION")
    print("=" * 75)

    test_expressions = [
        "A+B*C",
        "(A+B)*C",
        "A+B*(C^D-E)^(F+G*H)-I",
        "((A+B)*C-(D-E))^(F+G)",
        "K+L-M*N+(O^P)*W/U/V*T+Q"
    ]

    for expr in test_expressions:
        post = infix_to_postfix(expr)
        pre = infix_to_prefix(expr)
        print(f"Infix:   {expr}")
        print(f"Postfix: {post}")
        print(f"Prefix:  {pre}")
        print("-" * 75)

    # Detailed table trace for standard college exam problem
    infix_to_postfix("A+B*(C-D)/E", trace=True)
