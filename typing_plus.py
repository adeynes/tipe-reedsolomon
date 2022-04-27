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

    def __truediv__(self, other) -> Number:
        ...


class Real(Number):
    v: int

    def __init__(self, v):
        self.v = v

    @classmethod
    def zero(cls) -> Real:
        return Real(0)

    @classmethod
    def one(cls) -> Real:
        return Real(1)

    def __eq__(self, other) -> bool:
        return self.v == other.v

    def __neg__(self) -> Real:
        return Real(-self.v)

    def __add__(self, other) -> Real:
        return Real(self.v + other.v)

    def __sub__(self, other) -> Real:
        return Real(self.v - other.v)

    def __mul__(self, other) -> Number:
        return Real(self.v * other.v)

    def __truediv__(self, other) -> Number:
        return Real(self.v / other.v)

    def __str__(self):
        return str(self.v)
