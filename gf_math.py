from __future__ import annotations
from typing import *
from poly_math import Polynomial
from typing_plus import Number


class F2(Number):
    p: int = 2
    m: int = 1
    q: int = 2 ** m
    bin_rep: bool

    def __init__(self, bin_rep: bool):
        self.bin_rep = bin_rep

    @staticmethod
    def zero() -> F2:
        return F2(False)

    @staticmethod
    def one() -> F2:
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

    def __pow__(self, power, modulo=None) -> F2:
        assert power >= 0
        if self == F2.zero() and power > 0:
            return F2.zero()
        else:
            return F2.one()

    def __str__(self) -> str:
        return "1" if self.bin_rep else "0"


class F256(Number):
    p: int = 2
    m: int = 8
    q: int = p ** m
    bin_rep: int

    EXP: List[F256] = []
    LOG: List[Optional[int]] = [None] + [0] * 255

    def __init__(self, bin_rep: int):
        assert 0 <= bin_rep <= self.q - 1
        self.bin_rep = bin_rep

    @staticmethod
    def zero() -> F256:
        return F256(0)

    @staticmethod
    def one() -> F256:
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

    def mul_internal__(self, other) -> F256:
        return F256.from_poly(self.to_poly() * other.to_poly())

    def __mul__(self, other) -> F256:
        if self == F256.zero() or other == F256.zero():
            return F256.zero()
        else:
            return F256.EXP[(F256.LOG[self.bin_rep] + F256.LOG[other.bin_rep]) % 255]

    def pow_internal__(self, power) -> F256:
        assert power >= 0
        return F256.one() if power == 0 else self.mul_internal__(self.pow_internal__(power - 1))

    def __pow__(self, power, modulo=None) -> F256:
        assert power >= 0
        return F256.one() if power == 0 else self * (self ** (power-1))

    def __str__(self) -> str:
        return str(self.bin_rep)

    @staticmethod
    def Reducer_Polynomial() -> Polynomial[F2]:
        # 0x11d, this is a standard primitive polynomial
        return Polynomial[F2](F2, [F2.one(), F2.zero(), F2.one(), F2.one(), F2.one(), F2.zero(), F2.zero(), F2.zero(), F2.one()])

    @staticmethod
    def Generator() -> F256:
        return F256(2)


def f256_precalc():
    for i in range(255):
        x = F256.Generator().pow_internal__(i)
        F256.EXP.append(x)
        F256.LOG[x.bin_rep] = i


f256_precalc()
