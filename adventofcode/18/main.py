from __future__ import annotations
from typing import Any

import fire
import numpy as np
from adventofcode.helper.io import (
    get_day,
    get_example_input,
    get_riddle_input,
    save_riddle_input,
)
from numpy.typing import NDArray


def f(direction) -> NDArray[Any]:
    match direction:
        case "R":
            return np.array([0, 1])
        case "L":
            return np.array([0, -1])
        case "U":
            return np.array([-1, 0])
        case "D":
            return np.array([1, 0])
        case _:
            raise KeyError


def riddle1(riddle_input: str) -> int | str:
    answer = 0

    positions = [np.array([0, 0])]
    for i, line in enumerate(riddle_input.splitlines()):
        direction, length, color = line.split(" ")
        length = int(length)
        color = color[1:-1]
        dv = f(direction)
        for _ in range(length):
            positions.append(positions[-1] + dv)
    positions = np.array(positions)
    positions = positions - np.min(positions, axis=0)
    M = np.zeros(np.max(positions, axis=0) + 1, dtype=int)
    M[positions[:, 0], positions[:, 1]] = 1

    M[0, 0] = -1
    M[0, 330] = -1
    M[250, 0] = -1
    M[250, 250] = -1

    for _ in range(np.max(M.shape)):
        # print(_)
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                if M[i, j] == -1:
                    for di, dj in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                        ibar, jbar = i + di, j + dj
                        if 0 <= ibar < M.shape[0] and 0 <= jbar < M.shape[1]:
                            if M[ibar, jbar] == 0:
                                M[ibar, jbar] = -1
    # print(len(np.argwhere(M == -1)))
    # print(len(np.argwhere(M == 1)))
    # print(len(np.argwhere(M == 0)))
    # print(np.prod(M.shape))
    return len(np.argwhere(M == 0)) + len(np.argwhere(M == 1))
    # fig, ax = plt.subplots()
    # ax.imshow(M)
    # # ax.scatter(positions[:, 0], positions[:, 1])
    # plt.show()


def riddle2(riddle_input: str) -> int | str:
    answer = 0
    map_direction = {"0": "R", "1": "D", "2": "L", "3": "U"}

    convex_hull = [np.array([0, 0])]
    for i, line in enumerate(riddle_input.splitlines()):
        _, _, hex = line.split(" ")
        hex = hex[1:-1]
        stephex, direction = hex[:-1], hex[-1]
        step = int(stephex[1:], 16)
        direction = map_direction[direction]
        convex_hull.append(convex_hull[-1] + step * f(direction))
    convex_hull = np.array(convex_hull)

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
    return a + b // 2 + 1


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
