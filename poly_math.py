from __future__ import annotations
from typing_plus import *

KT = TypeVar('KT', bound=Number)


# A polynomial in K[X] is a P: List[K] where P[i] is the coefficient of X^i:
# In Z[X], [-2, 0, 4, 1] represents X^3 + 4X^2 - 2

class Polynomial(Generic[KT]):
    K: Type[KT]
    coeffs: List[KT]

    def __init__(self, K: Type[KT], coeffs: List[KT]):
        self.K = K
        self.coeffs = coeffs
        self.normalize()

    @staticmethod
    def zero(K: Type[KT]) -> Polynomial[KT]:
        return Polynomial(K, [K.zero()])

    @staticmethod
    def constant(K: Type[KT], a: KT) -> Polynomial[KT]:
        return Polynomial(K, [a])

    # returns X^n
    @staticmethod
    def Xn(K: Type[KT], n: int) -> Polynomial:
        return Polynomial(K, [K.zero() for _ in range(n)] + [K.one()])

    def normalize(self) -> NoReturn:
        while self.coeffs != [] and self.coeffs[-1] == self.K.zero():
            self.coeffs.pop()

        if self.coeffs == []:
            self.coeffs = [self.K.zero()]  # The polynomial 0 is of degree 0, not -inf

    def is_zero(self):
        return self.coeffs == [self.K.zero()]

    def deg(self) -> int:
        return len(self.coeffs) - 1

    def eval(self, x: KT) -> KT:
        y = self.coeffs[-1]
        for i in range(1, self.deg() + 1):
            y = y * x + self.coeffs[self.deg()-i]

        return y

    def __neg__(self) -> Polynomial[KT]:
        return Polynomial(self.K, [-c for c in self.coeffs])

    def __add__(self, other: Polynomial[KT]) -> Polynomial[KT]:
        m = max(self.deg(), other.deg())
        sum_coeffs: List[KT] = []
        for i in range(m+1):
            sum_coeffs.append(self.K.zero())
            if i <= self.deg():
                sum_coeffs[i] += self.coeffs[i]
            if i <= other.deg():
                sum_coeffs[i] += other.coeffs[i]

        return Polynomial(self.K, sum_coeffs)

    def __sub__(self, other: Polynomial[KT]) -> Polynomial[KT]:
        return self + (-other)

    def __mul__(self, other: Polynomial[KT]) -> Polynomial[KT]:
        prod_coeffs: List[KT] = [self.K.zero() for _ in range(self.deg() + other.deg() + 1)]

        for i in range(self.deg()+1):
            for j in range(other.deg()+1):
                prod_coeffs[i + j] += self.coeffs[i] * other.coeffs[j]

        return Polynomial(self.K, prod_coeffs)

    # cf Page 15, cours "Les Polynômes" (Merle HX2 LLG)
    def __divmod__(self, divisor: Polynomial[KT]) -> Tuple[Polynomial[KT], Polynomial[KT]]:
        assert not divisor.is_zero()

        n = self.deg()
        p = divisor.deg()
        a = self.coeffs[-1]

        assert divisor.coeffs[-1] == self.K.one()

        if self.is_zero():
            return Polynomial.zero(self.K), Polynomial.zero(self.K)

        if n == 0 and p == 0:
            return Polynomial(self.K, [a]), Polynomial.zero(self.K)

        if p > n:
            return Polynomial.zero(self.K), self

        C = Polynomial(self.K, self.coeffs[:-1])
        D = Polynomial(self.K, divisor.coeffs[:-1])

        E = Polynomial.constant(self.K, a)*Polynomial.Xn(self.K, n-p)
        F = C - E*D
        Q, R = divmod(F, divisor)
        return E + Q, R

    def __floordiv__(self, other):
        return divmod(self, other)[0]

    def __mod__(self, other):
        return divmod(self, other)[1]

    def __str__(self):
        out = ""
        for i in range(len(self.coeffs)):
            out += str(self.coeffs[i]) + "X^" + str(i) + "  "

        return out
