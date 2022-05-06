from typing import *

from gf_math import F256


def mult_column(M, Y):
    res = [F256.zero() for _ in range(len(M))]

    for i in range(len(M)):
        for j in range(len(Y)):
            res[i] += M[i][j] * Y[j]

    return res


def mult(M, N):
    res = [[F256.zero() for _ in range(len(N[0]))] for _ in range(len(M))]
    for i in range(len(M)):
        for j in range(len(N[0])):
            for k in range(len(N)):
                res[i][j] += M[i][k] * N[k][j]

    return res


def transpose_matrix(M):
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]


def matrix_minor(M, i, j):
    return [row[:j] + row[j+1:] for row in (M[:i] + M[i+1:])]


# Bareiss algorithm, see https://stackoverflow.com/questions/66192894/precise-determinant-of-integer-nxn-matrix
def det_f256(M: List[List[F256]]):
    M = [row[:] for row in M]  # make a copy to keep original M unmodified
    N, prev = len(M), F256.one()

    for i in range(N-1):
        if M[i][i] == F256.zero():  # swap with another row having nonzero i's elem
            swapto = next((j for j in range(i+1, N) if M[j][i] != F256.zero()), None)
            if swapto is None:
                return F256.zero()  # all M[*][i] are zero => zero determinant
            M[i], M[swapto] = M[swapto], M[i]

        for j in range(i+1, N):
            for k in range(i+1, N):
                M[j][k] = (M[j][k] * M[i][i] - M[j][i] * M[i][k]) * prev.inv()

        prev = M[i][i]

    return M[-1][-1]


def inv_f256(M: List[List[F256]]):
    det = det_f256(M)

    if len(M) == 1:
        return [[M[0][0].inv()]]

    if len(M) == 2:
        return [[M[1][1] * det.inv(), M[0][1] * det.inv()],
                [M[1][0] * det.inv(), M[0][0] * det.inv()]]

    cofactors = []

    for r in range(len(M)):
        cofactorRow = []
        for c in range(len(M)):
            minor = matrix_minor(M, r, c)
            cofactorRow.append(det_f256(minor))
        cofactors.append(cofactorRow)

    cofactors = transpose_matrix(cofactors)

    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]*det.inv()

    return cofactors
