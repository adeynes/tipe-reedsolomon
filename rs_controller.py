from __future__ import annotations
from math import *
import numpy as np
import matplotlib.image as mpimg
from rs_math import *


def split_str(msg: str, k: int) -> List[str]:
    l = len(msg)
    msgs: List[str] = []

    for i in range(l//k):
        msgs.append(msg[(k*i) : (k * (i+1))])

    msgs.append(msg[(k * (l//k)) :])

    return msgs


def encode_str(msg: str, n: int, t: int) -> List[Polynomial[F256]]:
    return [str_to_poly(atom) for atom in split_str(msg, n - 2*t)]


def split_image_png(path: str, n: int, t: int) -> List[List[F256]]:
    im = mpimg.imread(path)
    return split_image_internal__((255 * im[:, :, :3]).astype(np.uint8), n, t)


def split_image_jpg(path: str, n: int, t: int) -> List[List[F256]]:
    return split_image_internal__(mpimg.imread(path), n, t)


def split_image_internal__(im: List[List[List[int]]], n: int, t: int) -> List[List[F256]]:
    height = len(im)
    width = len(im[0])
    size = height * width
    k = n - 2*t
    pixels_per_atom = k//3
    atoms: List[List[F256]] = [[] for _ in range(ceil(size / pixels_per_atom))]

    def i_to_pq(i):
        return i // width, i % width

    for i in range(size):
        p, q = i_to_pq(i)
        for j in range(3):
            atoms[i // pixels_per_atom].append(F256(im[p][q][j]))

    return atoms
