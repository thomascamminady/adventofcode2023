from __future__ import annotations

import logging
import fire
from adventofcode.helper.io import get_day, get_riddle_input, save_riddle_input
import networkx as nx

DIMENSION = 140


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


def ij2idx(i: int, j: int) -> int:
    return i * DIMENSION + j


def idx2ij(idx) -> tuple[int, int]:
    return idx // DIMENSION, idx % DIMENSION


def riddle1(riddle_input: str) -> int | str:
    edges = []
    starti, startj = 0, 0
    chars = [[_ for _ in line] for line in riddle_input.splitlines()]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            c = chars[i][j]
            # print(i, j, c)
            # print(c == "S")

            for direction in connections(c):
                di, dj = where(direction)
                if 0 <= i + di < DIMENSION and 0 <= j + dj < DIMENSION:
                    if opposite(direction) in connections(chars[i + di][j + dj]):
                        edges.append((ij2idx(i + di, j + dj), ij2idx(i, j)))

            if c == "S":
                starti, startj = i, j
    # print(edges)
    # print(starti, startj)

    G = nx.from_edgelist(edges)
    return len(nx.find_cycle(G, ij2idx(starti, startj))) // 2


def riddle2(riddle_input: str) -> int | str:
    edges = []
    starti, startj = 0, 0
    chars = [[_ for _ in line] for line in riddle_input.splitlines()]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            c = chars[i][j]
            for direction in connections(c):
                di, dj = where(direction)
                if 0 <= i + di < DIMENSION and 0 <= j + dj < DIMENSION:
                    if opposite(direction) in connections(chars[i + di][j + dj]):
                        edges.append((ij2idx(i + di, j + dj), ij2idx(i, j)))

            if c == "S":
                starti, startj = i, j

    G = nx.from_edgelist(edges)
    cycle = nx.find_cycle(G, ij2idx(starti, startj), orientation="original")
    for i in range(1, len(cycle)):
        assert cycle[i - 1][1] == cycle[i][0]

    # print(cycle)
    nodes = []
    for e in cycle:
        nodes.append(e[0])
        nodes.append(e[1])

    nodes = list(set(nodes))

    import numpy as np

    M = np.zeros((DIMENSION, DIMENSION))
    for n, idx in enumerate(cycle):
        i, j = idx2ij(idx[0])
        M[i, j] = 1
        i, j = idx2ij(idx[1])
        M[i, j] = 1

    for c in cycle:
        oldi, oldj = idx2ij(c[0])
        newi, newj = idx2ij(c[1])

        print(oldi, oldj, newi, newj)

        # left
        direction = +1
        if newi == oldi + 1:
            print("down")
            # if M[newi, newj + 1] == 0:
            #     M[newi, newj + 1] = 2
            if M[newi - 1, newj + 1] == 0:
                M[newi - 1, newj + 1] = 2
        elif newi == oldi - 1:
            print("up")
            # if M[newi, newj - 1] == 0:
            #     M[newi, newj - 1] = 2
            if M[newi + 1, newj - 1] == 0:
                M[newi + 1, newj - 1] = 2
        elif newj == oldj + 1:
            print("right")
            # if M[newi - 1, newj] == 0:
            #     M[newi - 1, newj] = 2
            if M[newi - 1, newj - 1] == 0:
                M[newi - 1, newj - 1] = 2
        elif newj == oldj - 1:
            print("down")
            # if M[newi + 1, newj] == 0:
            #     M[newi + 1, newj] = 2
            if M[newi - 1, newj + 1] == 0:
                M[newi - 1, newj + 1] = 2
        else:
            raise ValueError

    # 535 too high
    # # spread
    for _ in range(150):
        for j in range(1, DIMENSION - 1):
            for i in range(1, DIMENSION - 1):
                if M[i, j] >= 2:
                    for deltai in [-1, 0, 1]:
                        for deltaj in [-1, 0, 1]:
                            if M[i + deltai, j + deltaj] == 0:
                                M[i + deltai, j + deltaj] = 3
    M[2, 2] = -1
    M[130, 2] = -1
    M[130, 130] = -1
    for _ in range(150):
        for j in range(1, DIMENSION - 1):
            for i in range(1, DIMENSION - 1):
                if M[i, j] == -1:
                    for deltai in [-1, 0, 1]:
                        for deltaj in [-1, 0, 1]:
                            if M[i + deltai, j + deltaj] > 1:
                                M[i + deltai, j + deltaj] = -1
    print(np.sum(M > 1))

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.imshow(M)
    plt.show()


def aoc(
    save: bool = True,
    show: bool = False,
    example: bool = False,
    log: bool = True,
):
    day = get_day(__file__)
    riddle_input = get_riddle_input(day)
    if log:
        logging.basicConfig(level=logging.INFO)
    if save:
        save_riddle_input(day, riddle_input)
    if show:
        print(riddle_input)
    if example:
        riddle_input = EXAMPLE

    answer1 = riddle1(riddle_input)
    print(answer1)

    if answer1 != 0:
        answer2 = riddle2(riddle_input)
        print(answer2)


# def print(_):
#     logging.info(_)


if __name__ == "__main__":
    fire.Fire(aoc)
