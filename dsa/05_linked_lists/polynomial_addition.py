"""
Experiment: Polynomial Representation and Operations using Linked List
-----------------------------------------------------------------------
Aim:
    To represent single-variable polynomials using Singly Linked Lists and
    perform Polynomial Addition and Polynomial Multiplication in Python.

Theory:
    A polynomial P(x) = c_n*x^e_n + ... + c_1*x^e_1 + c_0*x^e_0 can be naturally
    represented using a linked list where each node has:
    1. coeff: The numerical coefficient
    2. exp:   The power/exponent of the variable
    3. next:  Pointer to the next term in descending order of exponents.

    Addition Algorithm:
    - Compare exponents of terms at pointers p1 and p2:
      - If exp1 == exp2: Add coefficients (coeff1 + coeff2). Advance both.
      - If exp1 > exp2:  Append term from p1 to result. Advance p1.
      - If exp1 < exp2:  Append term from p2 to result. Advance p2.
    - Append any remaining terms.

    Multiplication Algorithm:
    - Multiply each term of the first polynomial with each term of the second
      polynomial (new_coeff = c1 * c2, new_exp = e1 + e2).
    - Insert and combine like terms into the result list.

Time Complexity:
    - Addition:       O(m + n) where m and n are the number of terms.
    - Multiplication: O(m * n * k) where k is terms in result.
"""

from typing import List, Optional, Tuple


class PolyNode:
    """Represents a single term in a polynomial (coeff * x^exp)."""
    def __init__(self, coeff: float, exp: int):
        self.coeff: float = coeff
        self.exp: int = exp
        self.next: Optional["PolyNode"] = None

    def __repr__(self):
        return f"{self.coeff}x^{self.exp}"


class Polynomial:
    """
    Polynomial linked list maintaining terms in strictly descending order of exponents.
    """
    def __init__(self):
        self.head: Optional[PolyNode] = None

    def insert_term(self, coeff: float, exp: int) -> None:
        """
        Inserts a term into the polynomial. If a term with the same exponent
        already exists, their coefficients are combined.
        """
        if coeff == 0:
            return

        new_node = PolyNode(coeff, exp)

        if self.head is None or self.head.exp < exp:
            new_node.next = self.head
            self.head = new_node
            return

        if self.head.exp == exp:
            self.head.coeff += coeff
            if self.head.coeff == 0:
                self.head = self.head.next
            return

        curr = self.head
        while curr.next and curr.next.exp > exp:
            curr = curr.next

        if curr.next and curr.next.exp == exp:
            curr.next.coeff += coeff
            if curr.next.coeff == 0:
                curr.next = curr.next.next
        else:
            new_node.next = curr.next
            curr.next = new_node

    def add(self, other: "Polynomial") -> "Polynomial":
        """
        Adds two polynomials and returns a new Polynomial instance.
        """
        result = Polynomial()
        p1 = self.head
        p2 = other.head

        while p1 and p2:
            if p1.exp == p2.exp:
                s = p1.coeff + p2.coeff
                if s != 0:
                    result.insert_term(s, p1.exp)
                p1 = p1.next
                p2 = p2.next
            elif p1.exp > p2.exp:
                result.insert_term(p1.coeff, p1.exp)
                p1 = p1.next
            else:
                result.insert_term(p2.coeff, p2.exp)
                p2 = p2.next

        while p1:
            result.insert_term(p1.coeff, p1.exp)
            p1 = p1.next

        while p2:
            result.insert_term(p2.coeff, p2.exp)
            p2 = p2.next

        return result

    def multiply(self, other: "Polynomial") -> "Polynomial":
        """
        Multiplies two polynomials and returns a new Polynomial instance.
        """
        result = Polynomial()
        p1 = self.head

        while p1:
            p2 = other.head
            while p2:
                c = p1.coeff * p2.coeff
                e = p1.exp + p2.exp
                result.insert_term(c, e)
                p2 = p2.next
            p1 = p1.next

        return result

    def to_string(self) -> str:
        """Formats the polynomial into standard algebraic notation."""
        if self.head is None:
            return "0"

        terms = []
        curr = self.head
        while curr:
            c = curr.coeff
            e = curr.exp

            # Coefficient formatting
            c_str = f"{c:g}"
            if e == 0:
                terms.append(f"{c_str}")
            elif e == 1:
                terms.append(f"{c_str}x" if c != 1 else "x")
            else:
                terms.append(f"{c_str}x^{e}" if c != 1 else f"x^{e}")

            curr = curr.next

        return " + ".join(terms).replace("+ -", "- ")

    def display(self) -> None:
        print(self.to_string())


if __name__ == "__main__":
    print("=" * 65)
    print("     COLLEGE DSA LAB: POLYNOMIAL ADDITION & MULTIPLICATION")
    print("=" * 65)

    # Polynomial 1: 5x^4 + 3x^2 + 2x + 7
    p1 = Polynomial()
    p1.insert_term(5, 4)
    p1.insert_term(3, 2)
    p1.insert_term(2, 1)
    p1.insert_term(7, 0)

    # Polynomial 2: 4x^3 - 3x^2 + 8
    p2 = Polynomial()
    p2.insert_term(4, 3)
    p2.insert_term(-3, 2)
    p2.insert_term(8, 0)

    print("Polynomial 1: ", end="")
    p1.display()
    print("Polynomial 2: ", end="")
    p2.display()

    # Addition
    sum_poly = p1.add(p2)
    print("\nP(x) + Q(x):  ", end="")
    sum_poly.display()

    # Multiplication: (2x + 3) * (4x^2 - 1)
    a = Polynomial()
    a.insert_term(2, 1)
    a.insert_term(3, 0)

    b = Polynomial()
    b.insert_term(4, 2)
    b.insert_term(-1, 0)

    print("\n--- Multiplication Test ---")
    print(f"A(x) = {a.to_string()}")
    print(f"B(x) = {b.to_string()}")
    prod_poly = a.multiply(b)
    print(f"A(x) * B(x) = {prod_poly.to_string()}")
