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
        delta = [v[3][0] - key[3][0], v[3][1] - key[3][1]]
        assert delta in [[0, 1], [0, -1], [-1, 0], [1, 0]]


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
                            M[value[0][0], value[0][1]]
                            + M[value[1][0], value[1][1]]
                            + M[value[2][0], value[2][1]]
                            + M[value[3][0], value[3][1]]
                        )
                        G.add_edge(key, value, weight=w)

    # print(G)
    _start = (0, 0)
    _end = (n, m)
    start_nodes = [_ for _ in G.nodes() if _start == _[0]]
    for node in start_nodes:
        G.add_edge((0, 0), node, weight=0)

    end_nodes = [_ for _ in G.nodes() if _end == _[-1]]
    for node in end_nodes:
        G.add_edge(node, (n, m), weight=0)

    path = nx.shortest_path(
        G,
        source=_start,
        target=_end,
        weight="weight",
    )
    for i, (pi, pj) in enumerate(zip(path[1:-2], path[2:-1])):
        assert pi[1] == pj[0]
        assert pi[2] == pj[1]
        assert pi[3] == pj[2]

    nodes = []
    for p in path[1:-1]:
        nodes.extend(list(p))
    nodes = set(nodes)
    nodes.remove((0, 0))
    return sum([M[i, j] for i, j in nodes])  # type:ignore


def riddle2(riddle_input: str) -> int | str:
    M = input_to_int_matrix(riddle_input)
    print(M.shape)

    def find_paths(N):
        def is_valid(x, y):
            return 0 <= x <= N and 0 <= y <= N

        def backtrack(x, y, path, is_horizontal):
            if x == N and y == N:
                paths.append(path.copy())
                return

            step_range = range(4, 11)
            if is_horizontal:
                for step in step_range:
                    if is_valid(x + step, y):
                        backtrack(
                            x + step, y, path + [(x + step, y)], not is_horizontal
                        )
            else:
                for step in step_range:
                    if is_valid(x, y + step):
                        backtrack(
                            x, y + step, path + [(x, y + step)], not is_horizontal
                        )

        paths = []
        backtrack(0, 0, [(0, 0)], True)  # Start with a horizontal move
        return paths

    # Example Usage
    N = 40  # Replace with the desired N value
    paths = find_paths(N)
    print("Number of paths:", len(paths))
    for path in paths[:5]:  # Print first 5 paths as an example
        print(path)

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

    # answer1 = riddle1(riddle_input)
    # print(answer1)

    answer2 = riddle2(riddle_input)
    print(answer2)


if __name__ == "__main__":
    fire.Fire(aoc)

    # 964 too high
    # 962 too high
    # 959
    # 903 wrong
