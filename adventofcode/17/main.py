from __future__ import annotations

import fire
from rich import print
from adventofcode.helper.io import (
    get_day,
    get_example_input,
    get_riddle_input,
    input_to_int_matrix,
    save_riddle_input,
)
import networkx as nx
import numpy as np

CONNECTIONS = {
    ((-3, 0), (-2, 0), (-1, 0), (0, 0)): [
        [(-2, 0), (-1, 0), (0, 0), (0, -1)],
        [(-2, 0), (-1, 0), (0, 0), (0, 1)],
    ],
    ((-2, -1), (-2, 0), (-1, 0), (0, 0)): [
        [(-2, 0), (-1, 0), (0, 0), (1, 0)],
        [(-2, 0), (-1, 0), (0, 0), (0, -1)],
        [(-2, 0), (-1, 0), (0, 0), (0, 1)],
    ],
    ((-2, 1), (-2, 0), (-1, 0), (0, 0)): [
        [(-2, 0), (-1, 0), (0, 0), (1, 0)],
        [(-2, 0), (-1, 0), (0, 0), (0, -1)],
        [(-2, 0), (-1, 0), (0, 0), (0, 1)],
    ],
    ((-2, -1), (-1, -1), (-1, 0), (0, 0)): [
        [(-1, -1), (-1, 0), (0, 0), (1, 0)],
        [(-1, -1), (-1, 0), (0, 0), (0, -1)],
        [(-1, -1), (-1, 0), (0, 0), (0, 1)],
    ],
    ((0, -1), (-1, -1), (-1, 0), (0, 0)): [
        [(-1, -1), (-1, 0), (0, 0), (1, 0)],
        [(-1, -1), (-1, 0), (0, 0), (0, 1)],
    ],
    ((-1, -2), (-1, -1), (-1, 0), (0, 0)): [
        [(-1, -1), (-1, 0), (0, 0), (1, 0)],
        [(-1, -1), (-1, 0), (0, 0), (0, -1)],
        [(-1, -1), (-1, 0), (0, 0), (0, 1)],
    ],
    ((-2, 1), (-1, 1), (-1, 0), (0, 0)): [
        [(-1, 1), (-1, 0), (0, 0), (1, 0)],
        [(-1, 1), (-1, 0), (0, 0), (0, -1)],
        [(-1, 1), (-1, 0), (0, 0), (0, 1)],
    ],
    ((0, 1), (-1, 1), (-1, 0), (0, 0)): [
        [(-1, 1), (-1, 0), (0, 0), (1, 0)],
        [(-1, 1), (-1, 0), (0, 0), (0, -1)],
    ],
    ((-1, 2), (-1, 1), (-1, 0), (0, 0)): [
        [(-1, 1), (-1, 0), (0, 0), (1, 0)],
        [(-1, 1), (-1, 0), (0, 0), (0, -1)],
        [(-1, 1), (-1, 0), (0, 0), (0, 1)],
    ],
    ((3, 0), (2, 0), (1, 0), (0, 0)): [
        [(2, 0), (1, 0), (0, 0), (0, -1)],
        [(2, 0), (1, 0), (0, 0), (0, 1)],
    ],
    ((2, -1), (2, 0), (1, 0), (0, 0)): [
        [(2, 0), (1, 0), (0, 0), (-1, 0)],
        [(2, 0), (1, 0), (0, 0), (0, -1)],
        [(2, 0), (1, 0), (0, 0), (0, 1)],
    ],
    ((2, 1), (2, 0), (1, 0), (0, 0)): [
        [(2, 0), (1, 0), (0, 0), (-1, 0)],
        [(2, 0), (1, 0), (0, 0), (0, -1)],
        [(2, 0), (1, 0), (0, 0), (0, 1)],
    ],
    ((0, -1), (1, -1), (1, 0), (0, 0)): [
        [(1, -1), (1, 0), (0, 0), (-1, 0)],
        [(1, -1), (1, 0), (0, 0), (0, 1)],
    ],
    ((2, -1), (1, -1), (1, 0), (0, 0)): [
        [(1, -1), (1, 0), (0, 0), (-1, 0)],
        [(1, -1), (1, 0), (0, 0), (0, -1)],
        [(1, -1), (1, 0), (0, 0), (0, 1)],
    ],
    ((1, -2), (1, -1), (1, 0), (0, 0)): [
        [(1, -1), (1, 0), (0, 0), (-1, 0)],
        [(1, -1), (1, 0), (0, 0), (0, -1)],
        [(1, -1), (1, 0), (0, 0), (0, 1)],
    ],
    ((0, 1), (1, 1), (1, 0), (0, 0)): [
        [(1, 1), (1, 0), (0, 0), (-1, 0)],
        [(1, 1), (1, 0), (0, 0), (0, -1)],
    ],
    ((2, 1), (1, 1), (1, 0), (0, 0)): [
        [(1, 1), (1, 0), (0, 0), (-1, 0)],
        [(1, 1), (1, 0), (0, 0), (0, -1)],
        [(1, 1), (1, 0), (0, 0), (0, 1)],
    ],
    ((1, 2), (1, 1), (1, 0), (0, 0)): [
        [(1, 1), (1, 0), (0, 0), (-1, 0)],
        [(1, 1), (1, 0), (0, 0), (0, -1)],
        [(1, 1), (1, 0), (0, 0), (0, 1)],
    ],
    ((-2, -1), (-1, -1), (0, -1), (0, 0)): [
        [(-1, -1), (0, -1), (0, 0), (-1, 0)],
        [(-1, -1), (0, -1), (0, 0), (1, 0)],
        [(-1, -1), (0, -1), (0, 0), (0, 1)],
    ],
    ((-1, -2), (-1, -1), (0, -1), (0, 0)): [
        [(-1, -1), (0, -1), (0, 0), (-1, 0)],
        [(-1, -1), (0, -1), (0, 0), (1, 0)],
        [(-1, -1), (0, -1), (0, 0), (0, 1)],
    ],
    ((-1, 0), (-1, -1), (0, -1), (0, 0)): [
        [(-1, -1), (0, -1), (0, 0), (1, 0)],
        [(-1, -1), (0, -1), (0, 0), (0, 1)],
    ],
    ((2, -1), (1, -1), (0, -1), (0, 0)): [
        [(1, -1), (0, -1), (0, 0), (-1, 0)],
        [(1, -1), (0, -1), (0, 0), (1, 0)],
        [(1, -1), (0, -1), (0, 0), (0, 1)],
    ],
    ((1, -2), (1, -1), (0, -1), (0, 0)): [
        [(1, -1), (0, -1), (0, 0), (-1, 0)],
        [(1, -1), (0, -1), (0, 0), (1, 0)],
        [(1, -1), (0, -1), (0, 0), (0, 1)],
    ],
    ((1, 0), (1, -1), (0, -1), (0, 0)): [
        [(1, -1), (0, -1), (0, 0), (-1, 0)],
        [(1, -1), (0, -1), (0, 0), (0, 1)],
    ],
    ((-1, -2), (0, -2), (0, -1), (0, 0)): [
        [(0, -2), (0, -1), (0, 0), (-1, 0)],
        [(0, -2), (0, -1), (0, 0), (1, 0)],
        [(0, -2), (0, -1), (0, 0), (0, 1)],
    ],
    ((1, -2), (0, -2), (0, -1), (0, 0)): [
        [(0, -2), (0, -1), (0, 0), (-1, 0)],
        [(0, -2), (0, -1), (0, 0), (1, 0)],
        [(0, -2), (0, -1), (0, 0), (0, 1)],
    ],
    ((0, -3), (0, -2), (0, -1), (0, 0)): [
        [(0, -2), (0, -1), (0, 0), (-1, 0)],
        [(0, -2), (0, -1), (0, 0), (1, 0)],
    ],
    ((-2, 1), (-1, 1), (0, 1), (0, 0)): [
        [(-1, 1), (0, 1), (0, 0), (-1, 0)],
        [(-1, 1), (0, 1), (0, 0), (1, 0)],
        [(-1, 1), (0, 1), (0, 0), (0, -1)],
    ],
    ((-1, 0), (-1, 1), (0, 1), (0, 0)): [
        [(-1, 1), (0, 1), (0, 0), (1, 0)],
        [(-1, 1), (0, 1), (0, 0), (0, -1)],
    ],
    ((-1, 2), (-1, 1), (0, 1), (0, 0)): [
        [(-1, 1), (0, 1), (0, 0), (-1, 0)],
        [(-1, 1), (0, 1), (0, 0), (1, 0)],
        [(-1, 1), (0, 1), (0, 0), (0, -1)],
    ],
    ((2, 1), (1, 1), (0, 1), (0, 0)): [
        [(1, 1), (0, 1), (0, 0), (-1, 0)],
        [(1, 1), (0, 1), (0, 0), (1, 0)],
        [(1, 1), (0, 1), (0, 0), (0, -1)],
    ],
    ((1, 0), (1, 1), (0, 1), (0, 0)): [
        [(1, 1), (0, 1), (0, 0), (-1, 0)],
        [(1, 1), (0, 1), (0, 0), (0, -1)],
    ],
    ((1, 2), (1, 1), (0, 1), (0, 0)): [
        [(1, 1), (0, 1), (0, 0), (-1, 0)],
        [(1, 1), (0, 1), (0, 0), (1, 0)],
        [(1, 1), (0, 1), (0, 0), (0, -1)],
    ],
    ((-1, 2), (0, 2), (0, 1), (0, 0)): [
        [(0, 2), (0, 1), (0, 0), (-1, 0)],
        [(0, 2), (0, 1), (0, 0), (1, 0)],
        [(0, 2), (0, 1), (0, 0), (0, -1)],
    ],
    ((1, 2), (0, 2), (0, 1), (0, 0)): [
        [(0, 2), (0, 1), (0, 0), (-1, 0)],
        [(0, 2), (0, 1), (0, 0), (1, 0)],
        [(0, 2), (0, 1), (0, 0), (0, -1)],
    ],
    ((0, 3), (0, 2), (0, 1), (0, 0)): [
        [(0, 2), (0, 1), (0, 0), (-1, 0)],
        [(0, 2), (0, 1), (0, 0), (1, 0)],
    ],
}

for key, values in CONNECTIONS.items():
    for v in values:
        assert v[0] == key[1]
        assert v[1] == key[2]
        assert v[2] == key[3]


def offset_connections(
    i0, j0
) -> dict[
    tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]],
    list[tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]],
]:
    d = {}
    for key, values in CONNECTIONS.items():
        offset_key = tuple([(_[0] + i0, _[1] + j0) for _ in key])
        offset_values = []
        for value in values:
            offset_values.append(tuple([(_[0] + i0, _[1] + j0) for _ in value]))
        d[offset_key] = offset_values
    return d


def ij2idx(i: int, j: int, M) -> int:
    return i * M.shape[1] + j


def idx2ij(idx: int, M) -> tuple[int, int]:
    return idx // M.shape[1], idx % M.shape[1]


def riddle1(riddle_input: str) -> int | str:
    for key, values in CONNECTIONS.items():
        for v in values:
            assert v[0] == key[1]
            assert v[1] == key[2]
            assert v[2] == key[3]

    answer = 0

    M = input_to_int_matrix(riddle_input)
    n, m = M.shape[0] - 1, M.shape[1] - 1
    G = nx.DiGraph()
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            connections = offset_connections(i, j)
            for key, values in connections.items():
                for value in values:
                    is_valid = True
                    for _ in value:
                        if not (0 <= _[0] <= n and 0 <= _[1] <= m):
                            is_valid = False
                    if is_valid:
                        w = (
                            M[value[1][0], value[1][1]]
                            + M[value[2][0], value[2][1]]
                            + M[value[3][0], value[3][1]]
                        )
                        G.add_edge(key, value, weight=w)
    # print(G)
    start_nodes = [_ for _ in G.nodes() if (0, 0) == _[0]]
    for node in start_nodes:
        G.add_edge((0, 0), node, weight=0)

    end_nodes = [_ for _ in G.nodes() if (n, m) == _[-1]]
    for node in end_nodes:
        G.add_edge(node, (n, m), weight=0)

    path = nx.shortest_path(G, source=(0, 0), target=(n, m), weight="weight")
    print(path)
    for i, (pi, pj) in enumerate(zip(path[1:-2], path[2:-1])):
        print(i, pi, pj)
        assert pi[1] == pj[0]
        assert pi[2] == pj[1]
        assert pi[3] == pj[2]
    Y = np.zeros_like(M, dtype=str)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            Y[i, j] = str(M[i, j])
    nodes = []
    for node in path[1:-1]:
        # print(node)
        delta = [node[-1][0] - node[-2][0], node[-1][1] - node[-2][1]]
        if delta == [0, 1]:
            sign = ">"
        elif delta == [0, -1]:
            sign = "<"
        elif delta == [-1, 0]:
            sign = "^"
        elif delta == [1, 0]:
            sign = "v"
        else:
            raise ValueError
        for i, j in node:
            # Y[i, j] = "#"
            if (i, j) != (0, 0):
                nodes.append((i, j))
        Y[node[-1][0], node[-1][1]] = sign

    nodes_set = set(nodes)

    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            print(Y[i, j], end="")
        print()
    print(nodes)
    return sum([M[i, j] for i, j in nodes_set])
    # return answer


def riddle2(riddle_input: str) -> int | str:
    answer = 0

    for i, line in enumerate(riddle_input.splitlines()):
        pass

    return answer


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

    if answer1 != 0:
        answer2 = riddle2(riddle_input)
        print(answer2)


if __name__ == "__main__":
    fire.Fire(aoc)

    # 964 too high
    # 962 too high
    # 959
