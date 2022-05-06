from __future__ import annotations
from random import randrange
from poly_math import Polynomial, find_roots
from linalg_math import *


def Generator_Poly(t: int) -> Polynomial[F256]:
    G = Polynomial.one(F256)
    for i in range(1, 2*t+1):
        G *= Polynomial[F256](F256, [F256.Generator()**i, F256.one()])

    return G


# If A*X^2t = QG + (B%G) then C = A*X^2t + (B%G) = QG so G | C
def encode(A: Polynomial[F256], t: int) -> Polynomial[F256]:
    G = Generator_Poly(t)

    B = A * Polynomial.Xn(F256, 2*t)
    return B + (B % G)


def syndromes(D: Polynomial[F256], t: int) -> List[F256]:
    S = []
    for i in range(1, 2*t+1):
        S.append(D.eval(F256.Generator()**i))

    return S


def check(D: Polynomial[F256], t: int) -> bool:
    return syndromes(D, t) == ([F256.zero()] * (2*t))


def syndrome_matrix(S: List[F256], v: int) -> List[List[F256]]:
    M: List[List[F256]] = []
    for i in range(v):
        M.append([S[i+j] for j in range(v)])

    return M


def locator_poly(S: List[F256], t: int) -> Polynomial[F256]:
    for v in range(t, 0, -1):
        M = syndrome_matrix(S, v)
        if det_f256(M) == F256.zero():
            continue

        L_coeffs: List[F256] = mult_column(inv_f256(M), [-S[v+i] for i in range(v)])
        L_coeffs.reverse()
        return Polynomial[F256](F256, [F256.one()] + L_coeffs)


def error_locations(L: Polynomial[F256]) -> List[int]:
    return [(-F256.LOG[x.bin_rep]) % 255 for x in find_roots(F256, L)]


# https://en.wikipedia.org/wiki/Forney_algorithm
def error_values(S: List[F256], L: Polynomial[F256], t: int) -> List[F256]:
    S_poly = Polynomial[F256](F256, S)
    U = (S_poly * L) % Polynomial.Xn(F256, 2*t)
    er_locators_inv = find_roots(F256, L)

    return [U.eval(x) * L.derivative().eval(x).inv() for x in er_locators_inv]


def correct(D: Polynomial[F256], t: int) -> Polynomial[F256]:
    if check(D, t):
        return D

    S = syndromes(D, t)
    L = locator_poly(S, t)
    J = error_locations(L)
    Y = error_values(S, L, t)

    E_coeffs = [F256.zero() for _ in range(256)]
    for i in range(len(J)):
        # noinspection PyTypeChecker
        E_coeffs[J[i]] = Y[i]

    E = Polynomial[F256](F256, E_coeffs)

    return D - E


def extract_message(A: Polynomial[F256], t: int) -> Polynomial[F256]:
    return Polynomial[F256](F256, A.coeffs[(2 * t):])


def corrupt_message(msg: str, t: int, v: int) -> Polynomial[F256]:
    A = Polynomial[F256](F256, [F256(ord(x)) for x in msg])
    C = encode(A, t)

    for _ in range(v):
        C.coeffs[randrange(len(C.coeffs))] = F256(randrange(256))

    return C


def poly_to_message(A: Polynomial[F256]) -> str:
    return "".join([chr(x.bin_rep) for x in A.coeffs])
