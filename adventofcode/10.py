from __future__ import annotations

import logging
import fire
from adventofcode.helper.io import get_day, get_riddle_input, save_riddle_input
import networkx as nx

EXAMPLE = """"""


# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.


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
    return i * 140 + j


def idx2ij(idx) -> tuple[int, int]:
    return idx // 140, idx % 140


def riddle1(riddle_input: str) -> int | str:
    edges = []
    starti, startj = 0, 0
    chars = [[_ for _ in line] for line in riddle_input.splitlines()]
    for i in range(140):
        for j in range(140):
            c = chars[i][j]
            for direction in connections(c):
                di, dj = where(direction)
                if 0 <= i + di < 140 and 0 <= j + dj < 140:
                    if opposite(direction) in connections(chars[i + di][j + dj]):
                        edges.append((ij2idx(i + di, j + dj), ij2idx(i, j)))

            if c == "S":
                starti, startj = i, j

    G = nx.from_edgelist(edges)
    return len(nx.find_cycle(G, ij2idx(starti, startj))) // 2


def riddle2(riddle_input: str) -> int | str:
    edges = []
    starti, startj = 0, 0
    chars = [[_ for _ in line] for line in riddle_input.splitlines()]
    for i in range(140):
        for j in range(140):
            c = chars[i][j]
            for direction in connections(c):
                di, dj = where(direction)
                if 0 <= i + di < 140 and 0 <= j + dj < 140:
                    if opposite(direction) in connections(chars[i + di][j + dj]):
                        edges.append((ij2idx(i + di, j + dj), ij2idx(i, j)))

            if c == "S":
                starti, startj = i, j

    G = nx.from_edgelist(edges)
    cycle = nx.find_cycle(G, ij2idx(starti, startj))
    nodes = []
    for e in cycle:
        nodes.append(e[0])
        nodes.append(e[1])
    nodes = list(set(nodes))
    nodesij = [idx2ij(_) for _ in nodes]

    inside = find_squares_inside_curve(140, nodesij)

    print(nodes)
    import numpy as np

    M = np.zeros((140, 140))
    for idx in cycle:
        i, j = idx2ij(idx[0])
        M[i, j] = 1
        i, j = idx2ij(idx[1])
        M[i, j] = 1
    for i, j in inside:
        M[i, j] = 2
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
