from __future__ import annotations

import fire
import numpy as np
from adventofcode.helper.io import (
    get_day,
    get_example_input,
    get_riddle_input,
    save_riddle_input,
)
from scipy.sparse import csr_matrix
from numpy.typing import NDArray
import networkx as nx


def create_bool_matrix_vector(
    M: NDArray
) -> tuple[NDArray[np.bool_], NDArray[np.bool_]]:
    def ij2idx(i: int, j: int) -> int:
        return i * M.shape[1] + j

    A = np.zeros((M.size, M.size), dtype=np.bool_)
    start = 0
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            A[ij2idx(i, j), ij2idx(i, j)] = False
            if M[i, j] == "S":
                start = ij2idx(i, j)
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if 0 <= i + di < M.shape[0] and 0 <= j + dj < M.shape[1]:
                    ibar = (i + di) % M.shape[0]
                    jbar = (j + dj) % M.shape[1]

                    if M[i, j] in [".", "S"] and M[ibar, jbar] in [".", "S"]:
                        A[ij2idx(i, j), ij2idx(ibar, jbar)] = True
    x = np.zeros(M.size, dtype=np.bool_)
    x[start] = True
    return A, x


def riddle1(riddle_input: str) -> int | str:
    M = np.array([[_ for _ in line] for line in riddle_input.splitlines()])

    A, x = create_bool_matrix_vector(M)

    # make matrix sparse to speed up multiplication
    Asparse = csr_matrix(A)
    for _ in range(64):
        x = Asparse @ x

    return np.sum(x, dtype=int)


def riddle2(riddle_input: str) -> int | str:
    M = np.array([[_ for _ in line] for line in riddle_input.splitlines()])
    # n fold
    print(M.shape)
    M = np.vstack([M, M, M, M, M])
    M = np.hstack([M, M, M, M, M])
    spositions = np.argwhere(M == "S")
    for idx, (i, j) in enumerate(spositions):
        if idx != len(spositions) // 2:
            M[i, j] = "."
    print(M.shape)

    def ij2idx(i: int, j: int) -> int:
        return i * M.shape[0] + j

    def idx2ij(idx: int) -> tuple[int, int]:
        return idx // M.shape[1], idx % M.shape[1]

    A, x = create_bool_matrix_vector(M)
    G = nx.Graph()
    start = 0
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if M[i, j] == "S":
                start = ij2idx(i, j)
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if 0 <= i + di < M.shape[0] and 0 <= j + dj < M.shape[1]:
                    ibar = (i + di) % M.shape[0]
                    jbar = (j + dj) % M.shape[1]
                    if M[i, j] in [".", "S"] and M[ibar, jbar] in [".", "S"]:
                        G.add_edge(ij2idx(i, j), ij2idx(ibar, jbar))
    shortest_path = nx.shortest_path_length(G, start)

    I = np.zeros_like(M, dtype=np.int_)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if M[i, j] == "#":
                I[i, j] = -1
    for p, d in shortest_path.items():
        i, j = idx2ij(p)
        I[i, j] = d
    # I[I == 327] = 4000

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    print(np.min(I[:, 0]))
    print(np.max(I[:, 0]))
    print(np.min(I[:, -1]))
    print(np.max(I[:, -1]))
    print(np.min(I[0, :]))
    print(np.max(I[0, :]))
    print(np.min(I[-1, :]))
    print(np.max(I[-1, :]))
    print(I)
    ax.contour(I)
    plt.show()

    return 0


def aoc(save: bool = True, show: bool = False, example: bool = False) -> None:
    day = get_day(__file__)
    if example:
        riddle_input = get_example_input(day)
    else:
        riddle_input = get_riddle_input(day)
    if save and not example:
        save_riddle_input(day, riddle_input)
    if show:
        print(riddle_input)

    answer1 = riddle1(riddle_input)
    print(answer1)

    answer2 = riddle2(riddle_input)
    print(answer2)


if __name__ == "__main__":
    fire.Fire(aoc)
