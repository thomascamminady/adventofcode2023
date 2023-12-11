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


def ij2idx(i, j):
    return i * 140 + j


def riddle1(riddle_input: str) -> int | str:
    answer = 0

    edges = []
    starti, startj = 0, 0

    charts = [[_ for _ in line] for line in riddle_input.splitlines()]
    n = len(charts)
    for i in range(n):
        for j in range(n):
            c = charts[i][j]
            if c == ".":
                continue
            elif c == "|":
                edges.append((ij2idx(i - 1, j), ij2idx(i, j)))
                edges.append((ij2idx(i, j), ij2idx(i + 1, j)))
            elif c == "-":
                edges.append((ij2idx(i, j - 1), ij2idx(i, j)))
                edges.append((ij2idx(i, j), ij2idx(i, j + 1)))
            elif c == "L":
                edges.append((ij2idx(i - 1, j), ij2idx(i, j)))
                edges.append((ij2idx(i, j), ij2idx(i, j + 1)))
            elif c == "J":
                edges.append((ij2idx(i - 1, j), ij2idx(i, j)))
                edges.append((ij2idx(i, j), ij2idx(i, j - 1)))
            elif c == "7":
                edges.append((ij2idx(i, j - 1), ij2idx(i, j)))
                edges.append((ij2idx(i, j), ij2idx(i + 1, j)))
            elif c == "F":
                edges.append((ij2idx(i, j + 1), ij2idx(i, j)))
                edges.append((ij2idx(i, j), ij2idx(i + 1, j)))
            elif c == "S":
                starti, startj = i, j

    if charts[starti - 1][startj + 0] in (["|", "7", "F"]):
        print("down")
        edges.append((ij2idx(starti, startj), ij2idx(starti - 1, startj)))
    if charts[starti + 1][startj + 0] in (["|", "L", "J"]):
        print("up")
        edges.append((ij2idx(starti, startj), ij2idx(starti + 1, startj)))
    if charts[starti][startj - 1] in (["-", "F", "L"]):
        print("left")
        edges.append((ij2idx(starti, startj), ij2idx(starti, startj - 1)))
    if charts[starti][startj + 1] in (["-", "7", "J"]):
        print("right")
        edges.append((ij2idx(starti, startj), ij2idx(starti, startj + 1)))

    G = nx.from_edgelist(edges)
    print(nx.find_cycle(G, ij2idx(starti, startj)))
    return len(nx.find_cycle(G, ij2idx(starti, startj))) // 2

    import matplotlib.pyplot as plt

    plt.show()
    return answer


def riddle2(riddle_input: str) -> int | str:
    answer = 0

    for i, line in enumerate(riddle_input.splitlines()):
        pass

    return answer


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
