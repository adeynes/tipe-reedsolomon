from __future__ import annotations
from poly_math import Polynomial
from typing_plus import Number


class F2(Number):
    p: int = 2
    m: int = 1
    q: int = 2 ** m
    bin_rep: bool

    def __init__(self, bin_rep: bool):
        self.bin_rep = bin_rep

    @classmethod
    def zero(cls) -> F2:
        return F2(False)

    @classmethod
    def one(cls) -> F2:
        return F2(True)

    def __eq__(self, other) -> bool:
        return self.bin_rep == other.bin_rep

    def __neg__(self) -> F2:
        return F2(self.bin_rep)

    def __add__(self, other) -> F2:
        return F2(self.bin_rep ^ other.bin_rep)

    def __sub__(self, other) -> F2:
        return self + other

    def __mul__(self, other) -> F2:
        return F2(self.bin_rep & other.bin_rep)

    def __str__(self) -> str:
        return "1" if self.bin_rep else "0"


class F256(Number):
    p: int = 2
    m: int = 8
    q: int = 2 ** m
    bin_rep: int

    def __init__(self, bin_rep: int):
        assert 0 <= bin_rep <= self.q - 1
        self.bin_rep = bin_rep

    @classmethod
    def zero(cls) -> Number:
        return F256(0)

    @classmethod
    def one(cls) -> Number:
        return F256(1)

    @staticmethod
    def from_poly(polynomial: Polynomial[F2]) -> F256:
        P = polynomial % F256.Reducer_Polynomial()
        bin_rep = 0
        for i in range(P.deg() + 1):
            bin_rep += (P.coeffs[i].bin_rep << i)

        return F256(bin_rep)

    def to_poly(self) -> Polynomial[F2]:
        return Polynomial[F2](F2, [F2(bool((self.bin_rep >> i) % 2)) for i in range(self.m)])

    def __eq__(self, other) -> bool:
        return self.bin_rep == other.bin_rep

    def __neg__(self) -> F256:
        return F256(self.bin_rep)

    def __add__(self, other) -> F256:
        return F256(self.bin_rep ^ other.bin_rep)

    def __sub__(self, other) -> F256:
        return self + other

    def __mul__(self, other) -> F256:
        return F256.from_poly(self.to_poly() * other.to_poly())

    def __str__(self) -> str:
        return str(self.bin_rep)

    @staticmethod
    def Reducer_Polynomial() -> Polynomial[F2]:
        return Polynomial[F2](F2, [F2.one(), F2.zero(), F2.one(), F2.one(), F2.one(), F2.zero(), F2.zero(), F2.zero(), F2.one()])  # this is a standard choice

    @staticmethod
    def Generator() -> F256:
        return F256(2)
