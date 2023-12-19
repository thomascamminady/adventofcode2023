from __future__ import annotations

import fire
from adventofcode.helper.io import (
    get_day,
    get_example_input,
    get_riddle_input,
    save_riddle_input,
)

import networkx as nx


def connections(char: str) -> list[str]:
    match char:
        case "|":
            return ["u", "d"]
        case "-":
            return ["l", "r"]
        case "L":
            return ["u", "r"]
        case "J":
            return ["u", "l"]
        case "7":
            return ["l", "d"]
        case "F":
            return ["r", "d"]
        case "S":
            return ["u", "d", "l", "r"]
        case ".":
            return []
        case _:
            raise KeyError


def opposite(dir: str) -> str:
    match dir:
        case "u":
            return "d"
        case "d":
            return "u"
        case "l":
            return "r"
        case "r":
            return "l"
        case _:
            raise KeyError


def where(dir: str) -> tuple[int, int]:
    match dir:
        case "u":
            return (-1, 0)
        case "d":
            return (1, 0)
        case "l":
            return (0, -1)
        case "r":
            return (0, 1)
        case _:
            raise KeyError


def ij2idx(i: int, j: int, dimj) -> int:
    return i * dimj + j


def idx2ij(idx, dimj) -> tuple[int, int]:
    return idx // dimj, idx % dimj


def riddle1(riddle_input: str) -> int | str:
    edges = []
    starti, startj = 0, 0
    chars = [[_ for _ in line] for line in riddle_input.splitlines()]
    dimi, dimj = len(chars), len(chars[0])
    for i in range(dimi):
        for j in range(dimj):
            c = chars[i][j]
            # print(i, j, c)
            # print(c == "S")

            for direction in connections(c):
                di, dj = where(direction)
                if 0 <= i + di < dimi and 0 <= j + dj < dimj:
                    if opposite(direction) in connections(chars[i + di][j + dj]):
                        edges.append((ij2idx(i + di, j + dj, dimj), ij2idx(i, j, dimj)))

            if c == "S":
                starti, startj = i, j
    # print(edges)
    # print(starti, startj)

    G = nx.from_edgelist(edges)
    return len(nx.find_cycle(G, ij2idx(starti, startj, dimj))) // 2


def riddle2(riddle_input: str) -> int | str:
    edges = []
    starti, startj = 0, 0
    chars = [[_ for _ in line] for line in riddle_input.splitlines()]
    dimi, dimj = len(chars), len(chars[0])
    print(dimi, dimj)
    for i in range(dimi):
        for j in range(dimj):
            c = chars[i][j]
            for direction in connections(c):
                di, dj = where(direction)
                if 0 <= i + di < dimi and 0 <= j + dj < dimj:
                    if opposite(direction) in connections(chars[i + di][j + dj]):
                        edges.append((ij2idx(i + di, j + dj, dimj), ij2idx(i, j, dimj)))

            if c == "S":
                starti, startj = i, j

    G = nx.from_edgelist(edges)
    cycle = nx.find_cycle(G, ij2idx(starti, startj, dimj), orientation="original")
    for i in range(1, len(cycle)):
        assert cycle[i - 1][1] == cycle[i][0]

    # print(cycle)
    nodes = []
    for e in cycle:
        nodes.append(e[0])
        nodes.append(e[1])

    nodes = list(set(nodes))
    print(nodes)
    import numpy as np

    convex_hull = np.array([list(idx2ij(_, dimj)) for _ in nodes])

    def area_convex_hull(X, Y):
        n = len(X)
        area = 0
        perimeter = 0
        for i in range(n):
            j = (i + 1) % n  # Next vertex index (with wrap-around)
            area += X[i] * Y[j] - Y[i] * X[j]
            perimeter += abs(X[j] - X[i]) + abs(
                Y[j] - Y[i]
            )  # Manhattan distance (since only horizontal/vertical moves)

        return abs(area) // 2, perimeter

    a, b = area_convex_hull(convex_hull[:, 0], convex_hull[:, 1])
    print(a + b // 2 + 1, a)

    # M = np.zeros((DIMENSION, DIMENSION))
    # for n, idx in enumerate(cycle):
    #     i, j = idx2ij(idx[0])
    #     M[i, j] = 1
    #     i, j = idx2ij(idx[1])
    #     M[i, j] = 1

    # for c in cycle:
    #     oldi, oldj = idx2ij(c[0])
    #     newi, newj = idx2ij(c[1])

    #     print(oldi, oldj, newi, newj)

    #     # left
    #     direction = +1
    #     if newi == oldi + 1:
    #         print("down")
    #         # if M[newi, newj + 1] == 0:
    #         #     M[newi, newj + 1] = 2
    #         if M[newi - 1, newj + 1] == 0:
    #             M[newi - 1, newj + 1] = 2
    #     elif newi == oldi - 1:
    #         print("up")
    #         # if M[newi, newj - 1] == 0:
    #         #     M[newi, newj - 1] = 2
    #         if M[newi + 1, newj - 1] == 0:
    #             M[newi + 1, newj - 1] = 2
    #     elif newj == oldj + 1:
    #         print("right")
    #         # if M[newi - 1, newj] == 0:
    #         #     M[newi - 1, newj] = 2
    #         if M[newi - 1, newj - 1] == 0:
    #             M[newi - 1, newj - 1] = 2
    #     elif newj == oldj - 1:
    #         print("down")
    #         # if M[newi + 1, newj] == 0:
    #         #     M[newi + 1, newj] = 2
    #         if M[newi - 1, newj + 1] == 0:
    #             M[newi - 1, newj + 1] = 2
    #     else:
    #         raise ValueError

    # # 535 too high
    # # # spread
    # for _ in range(150):
    #     for j in range(1, DIMENSION - 1):
    #         for i in range(1, DIMENSION - 1):
    #             if M[i, j] >= 2:
    #                 for deltai in [-1, 0, 1]:
    #                     for deltaj in [-1, 0, 1]:
    #                         if M[i + deltai, j + deltaj] == 0:
    #                             M[i + deltai, j + deltaj] = 3
    # M[2, 2] = -1
    # M[130, 2] = -1
    # M[130, 130] = -1
    # for _ in range(150):
    #     for j in range(1, DIMENSION - 1):
    #         for i in range(1, DIMENSION - 1):
    #             if M[i, j] == -1:
    #                 for deltai in [-1, 0, 1]:
    #                     for deltaj in [-1, 0, 1]:
    #                         if M[i + deltai, j + deltaj] > 1:
    #                             M[i + deltai, j + deltaj] = -1
    # print(np.sum(M > 1))

    # import matplotlib.pyplot as plt

    # fig, ax = plt.subplots()
    # ax.imshow(M)
    # plt.show()


def aoc(
    save: bool = True,
    show: bool = False,
    example: bool = False,
    log: bool = True,
):
    day = get_day(__file__)
    if example:
        riddle_input = get_example_input(day)
    else:
        riddle_input = get_riddle_input(day)
    if save:
        save_riddle_input(day, riddle_input)
    if show:
        print(riddle_input)

    answer1 = riddle1(riddle_input)
    print(answer1)

    if answer1 != 0:
        answer2 = riddle2(riddle_input)
        print(answer2)


if __name__ == "__main__":
    fire.Fire(aoc)
