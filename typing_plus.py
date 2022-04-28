from __future__ import annotations
from typing import *


# TODO: ": Self" typehints when we get it in 3.11
# (can't typehint : Number currently because Liskov)

class Number(Protocol):
    @staticmethod
    def zero() -> Number:
        ...

    @staticmethod
    def one() -> Number:
        ...

    def __neg__(self) -> Number:
        ...

    def __add__(self, other) -> Number:
        ...

    def __sub__(self, other) -> Number:
        ...

    def __mul__(self, other) -> Number:
        ...

    def __pow__(self, power, modulo=None) -> Number:
        ...


class Int(Number):
    v: int

    def __init__(self, v):
        self.v = v

    @staticmethod
    def zero() -> Int:
        return Int(0)

    @staticmethod
    def one() -> Int:
        return Int(1)

    def __eq__(self, other) -> bool:
        return self.v == other.v

    def __neg__(self) -> Int:
        return Int(-self.v)

    def __add__(self, other) -> Int:
        return Int(self.v + other.v)

    def __sub__(self, other) -> Int:
        return Int(self.v - other.v)

    def __mul__(self, other) -> Int:
        return Int(self.v * other.v)

    def __pow__(self, power, modulo=None) -> Int:
        return Int(pow(self.v, power, modulo))

    def __str__(self):
        return str(self.v)
