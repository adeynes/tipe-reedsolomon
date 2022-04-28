from __future__ import annotations
from typing import *


# TODO: ": Self" typehints when we get it in 3.11
# (can't typehint : Number currently because Liskov)

class Number(Protocol):
    @classmethod
    def zero(cls) -> Number:
        ...

    @classmethod
    def one(cls) -> Number:
        ...

    def __neg__(self) -> Number:
        ...

    def __add__(self, other) -> Number:
        ...

    def __sub__(self, other) -> Number:
        ...

    def __mul__(self, other) -> Number:
        ...


class Int(Number):
    v: int

    def __init__(self, v):
        self.v = v

    @classmethod
    def zero(cls) -> Int:
        return Int(0)

    @classmethod
    def one(cls) -> Int:
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

    def __str__(self):
        return str(self.v)
