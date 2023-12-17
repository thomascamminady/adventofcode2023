from __future__ import annotations

import fire
import numpy as np
from typing import Literal
from adventofcode.helper.io import (
    get_day,
    get_example_input,
    get_riddle_input,
    save_riddle_input,
)


def velocity(
    k: int
) -> (
    tuple[Literal[-1], Literal[0]]
    | tuple[Literal[0], Literal[1]]
    | tuple[Literal[1], Literal[0]]
    | tuple[Literal[0], Literal[-1]]
):
    if k == 0:  # N
        return -1, 0
    elif k == 1:  # W
        return 0, 1
    elif k == 2:  # S
        return 1, 0
    else:  # E
        return 0, -1


def collision_kernel(k: int, gridij: str) -> tuple[int, int, int, int]:
    if gridij == ".":
        return (0, 0, 0, 0)
    elif k in [0, 2] and gridij == "|":
        return (0, 0, 0, 0)
    elif k in [1, 3] and gridij == "-":
        return (0, 0, 0, 0)
    elif k == 0 and gridij == "-":
        return (-1, 1, 0, 1)
    elif k == 2 and gridij == "-":
        return (0, 1, -1, 1)
    elif k == 1 and gridij == "|":
        return (1, -1, 1, 0)
    elif k == 3 and gridij == "|":
        return (1, 0, 1, -1)
    elif gridij == "/":
        if k == 0:
            return (-1, 1, 0, 0)
        elif k == 1:
            return (1, -1, 0, 0)
        elif k == 2:
            return (0, 0, -1, 1)
        elif k == 3:
            return (0, 0, 1, -1)
    elif gridij == "\\":
        if k == 0:
            return (-1, 0, 0, 1)
        elif k == 1:
            return (0, -1, 1, 0)
        elif k == 2:
            return (0, 1, -1, 0)
        elif k == 3:
            return (1, 0, 0, -1)
    raise ValueError


# def collision(i: int, j: int, k: int, gridij: str) -> list[tuple[int, int, int]]:
#     vi, vj = velocity(k)
#     print(gridij)
#     if gridij == ".":
#         return [(i, j, k)]
#     elif (k == 0 or k == 2) and gridij == "|":
#         return [(i + vi, j + vj, k)]
#     elif (k == 1 or k == 3) and gridij == "-":
#         return [(i + vi, j + vj, k)]
#     elif (k == 0 or k == 2) and gridij == "-":
#         return [(i, j - 1, 3), (i, j + 1, 1)]
#     elif (k == 1 or k == 3) and gridij == "|":
#         return [(i - 1, j, 0), (i + 1, j, 2)]
#     elif gridij == "/":
#         print("here")
#         if k == 0:
#             return [(i, j + 1, 1)]
#         elif k == 1:
#             return [(i - 1, j, 0)]
#         elif k == 2:
#             return [(i, j - 1, 3)]
#         elif k == 3:
#             return [(i + 1, j, 2)]
#         else:
#             raise KeyError

#     elif gridij == "\\":
#         if k == 0:
#             return [(i, j - 1, 3)]
#         elif k == 1:
#             return [(i + 1, j, 2)]
#         elif k == 2:
#             return [(i, j + 1, 1)]
#         elif k == 3:
#             return [(i - 1, j, 0)]
#         else:
#             raise KeyError
#     else:
#         raise KeyError


def riddle1(riddle_input: str) -> int | str:
    answer = 0

    grid = np.array([[_ for _ in line] for line in riddle_input.splitlines()])
    print(grid)
    psi = np.zeros((grid.shape[0], grid.shape[1], 4), dtype=int)

    def inbounds(i: int, j: int) -> bool:
        return (0 <= i < psi.shape[0]) and (0 <= j < psi.shape[1])

    history = np.zeros_like(grid, dtype=str)
    for i in range(history.shape[0]):
        for j in range(history.shape[1]):
            history[i, j] = "-"
    history[0, 0] = "#"

    psi[0, 0, 1] = 1
    print(history.shape)
    for n in range(100_000):
        if n == 0:
            for i in range(psi.shape[0]):
                for j in range(psi.shape[1]):
                    before = psi[i, j, :].copy()
                    for k, beforek in enumerate(before):
                        if beforek != 0:
                            change = collision_kernel(k, grid[i, j])
                            for l, changel in enumerate(change):
                                psi[i, j, l] += beforek * changel

        # print("\n\n")
        print(n, "  ", np.sum(history == "#"))
        new_psi = np.zeros_like(psi)
        for k in range(psi.shape[2]):
            vi, vj = velocity(k)
            for i in range(psi.shape[0]):
                for j in range(psi.shape[1]):
                    if psi[i, j, k] != 0:
                        if inbounds(i + vi, j + vj):
                            new_psi[i + vi, j + vj, k] += psi[i, j, k]
        psi = np.copy(new_psi)

        for i in range(psi.shape[0]):
            for j in range(psi.shape[1]):
                before = psi[i, j, :].copy()
                for k, beforek in enumerate(before):
                    if beforek != 0:
                        change = collision_kernel(k, grid[i, j])
                        for l, changel in enumerate(change):
                            psi[i, j, l] += beforek * changel
        for k in range(psi.shape[2]):
            for i in range(psi.shape[0]):
                for j in range(psi.shape[1]):
                    if psi[i, j, k] != 0:
                        history[i, j] = "#"
                        # history[i, j] = str(n % 10)
    print(history)
    return np.sum(history == "#")
    return answer


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
