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
    img = mpimg.imread(path)
    return split_img_internal__((255 * img[:, :, :3]).astype(np.uint8), n, t)


def split_image_jpg(path: str, n: int, t: int) -> List[List[F256]]:
    return split_img_internal__(mpimg.imread(path), n, t)


def split_img_internal__(img: List[List[List[int]]], n: int, t: int) -> List[List[F256]]:
    height = len(img)
    width = len(img[0])
    size = height * width
    k = n-2*t
    pixels_per_atom = k//3
    atoms: List[List[F256]] = [[] for _ in range(ceil(size / pixels_per_atom))]

    def i_to_pq(i):
        return i // width, i % width

    for i in range(size):
        p, q = i_to_pq(i)
        for j in range(3):
            atoms[i // pixels_per_atom].append(F256(img[p][q][j]))

    return atoms


def split_img_to_polys(atoms: List[List[F256]], k: int) -> List[Polynomial[F256]]:
    polys = []
    for atom in atoms:
        if len(atom) < k:
            atom += [F256.zero() for _ in range(len(atom)-k)]

        polys.append(Polynomial[F256](F256, atom))

    return polys


def polys_to_split_img(polys: List[Polynomial[F256]]) -> List[List[F256]]:
    return [A.coeffs for A in polys]


# TODO: this does not work
def split_img_to_img(atoms: List[List[F256]], height: int, width: int) -> List[List[List[int]]]:
    img = [[[] for _ in range(width)] for _ in range(height)]

    def i_to_pq(i):
        return i // width, i % width

    pixels = height * width
    i = 0
    for atom in atoms:
        for j in range(len(atom) // 3):
            p, q = i_to_pq(i)
            img[p][q] = [atom[j].bin_rep, atom[j+1].bin_rep, atom[j+2].bin_rep]
            i += 1

    return img


def corrupt_image_png(in_path: str, out_path: str, n: int, t: int, v: int) -> None:
    polys = split_img_to_polys(split_image_png(in_path, n, t), n-2*t)
    height, width, _ = mpimg.imread(in_path).shape

    corr_polys = []

    for A in polys:
        corr_polys.append(corrupt_poly(encode(A, t), v))

    mpimg.imsave(out_path, split_img_to_img(polys_to_split_img(corr_polys), height, width))


def corrupt_image_jpg(in_path: str, out_path: str, n: int, t: int, v: int) -> None:
    polys = split_img_to_polys(split_image_jpg(in_path, n, t), n-2*t)
    height, width, _ = mpimg.imread(in_path).shape

    corr_polys = []

    for A in polys:
        corr_polys.append(corrupt_poly(encode(A, t), v))

    mpimg.imsave(out_path, split_img_to_img(polys_to_split_img(corr_polys), height, width))

