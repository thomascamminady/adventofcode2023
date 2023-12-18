# from __future__ import annotations

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


def inbounds(i: int, j: int, psi) -> bool:
    return (0 <= i < psi.shape[0]) and (0 <= j < psi.shape[1])


def do_collision(psi, grid):
    indices = np.argwhere(np.sum(psi, 2) != 0)
    for i, j in indices:
        before = [_ for _ in psi[i, j, :]]
        for k, beforek in enumerate(before):
            if beforek != 0:
                change = collision_kernel(k, grid[i, j])
                for l, changel in enumerate(change):
                    psi[i, j, l] += beforek * changel
    return psi


def do_stream(psi, new_psi):
    indices = np.argwhere(np.sum(psi, 2) != 0)
    for k in range(psi.shape[2]):
        vi, vj = velocity(k)
        for i, j in indices:
            if psi[i, j, k] != 0:
                if inbounds(i + vi, j + vj, psi):
                    new_psi[i + vi, j + vj, k] += psi[i, j, k]
    return new_psi


def solve(i0, j0, k0, riddle_input) -> int:
    # from pyinstrument import Profiler

    # profiler = Profiler()
    # profiler.start()

    grid = np.array([[_ for _ in line] for line in riddle_input.splitlines()])
    psi = np.zeros((grid.shape[0], grid.shape[1], 4), dtype=int)

    history = np.zeros_like(grid, dtype=str)
    for i in range(history.shape[0]):
        for j in range(history.shape[1]):
            history[i, j] = "-"
    history[0, 0] = "#"

    psi[i0, j0, k0] = 1
    # print(history.shape)
    count = {}
    for n in range(1_000_000):
        if np.sum(psi) == 0:
            break
        if n == 0:
            psi = do_collision(psi, grid)
        # print("\n\n")
        count[n] = np.sum(history == "#")
        if n > 120:
            if count[n - 120] == count[n]:
                break

        new_psi = np.zeros_like(psi)
        new_psi = do_stream(psi, new_psi)
        psi = np.copy(new_psi)

        psi = do_collision(psi, grid)
        indices = np.argwhere(np.sum(psi, 2) != 0)
        for k in range(psi.shape[2]):
            for i, j in indices:
                if psi[i, j, k] != 0:
                    history[i, j] = "#"
                    # history[i, j] = str(n % 10)
    # profiler.stop()
    # profiler.print()
    # profiler.open_in_browser()
    return np.sum(history == "#")


def riddle1(riddle_input: str) -> int | str:
    z = solve(0, 0, 1, riddle_input)

    return z


def riddle2(riddle_input: str) -> int | str:
    results = []
    for j in range(110):
        z = solve(0, j, 2, riddle_input)
        print(j, z)
        results.append(z)
    for j in range(110):
        z = solve(109, j, 0, riddle_input)
        print(j, z)
        results.append(z)
    for i in range(110):
        z = solve(i, 0, 1, riddle_input)
        print(i, z)
        results.append(z)
    for i in range(110):
        z = solve(i, 109, 3, riddle_input)
        print(i, z)
        results.append(z)
    print(results)
    return max(results)


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
