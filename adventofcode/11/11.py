from __future__ import annotations

import logging
import fire
from adventofcode.helper.io import get_day, get_riddle_input, save_riddle_input
import numpy as np

EXAMPLE = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


def riddle1(riddle_input: str) -> int | str:
    answer = 0

    M = np.array(
        [[1 if _ == "#" else 0 for _ in line] for line in riddle_input.splitlines()]
    )
    sum0 = M.sum(axis=1)
    sum1 = M.sum(axis=0)
    expands0 = np.argwhere(sum0 == 0)
    expands1 = np.argwhere(sum1 == 0)

    newM = []
    m = len(M)
    for i in range(m):
        newM.append(M[i, :])
        if i in expands0:
            newM.append(M[i, :])
    M = np.array(newM)
    newM = []
    for j in range(m):
        newM.append(M[:, j])
        if j in expands1:
            newM.append(M[:, j])
    M = np.array(newM)
    # print(M.T)
    galaxies = np.argwhere(M == 1)

    def dist(ij0, ij1):
        return abs(ij0[0] - ij1[0]) + abs(ij0[1] - ij1[1])

    m = len(galaxies)
    # print(galaxies)
    # print(m)
    for i in range(m):
        for j in range(i):
            d = dist(galaxies[i], galaxies[j])
            # print(galaxies[i], galaxies[j], d)
            answer += d

    return answer


def riddle2(riddle_input: str) -> int | str:
    answer = 0

    M = np.array(
        [[1 if _ == "#" else 0 for _ in line] for line in riddle_input.splitlines()]
    )
    sum0 = M.sum(axis=1)
    sum1 = M.sum(axis=0)
    expands0 = np.argwhere(sum0 == 0)
    expands1 = np.argwhere(sum1 == 0)
    # print(expands0, expands1)

    def dist(ij0, ij1):
        return abs(ij0[0] - ij1[0]) + abs(ij0[1] - ij1[1])

    galaxies = np.argwhere(M == 1)

    expanded_galaxies = []
    for galaxy in galaxies:
        N = 1_000_000
        expanded_galaxies.append(
            [
                galaxy[0] + (N - 1) * np.sum(galaxy[0] > expands0),
                galaxy[1] + (N - 1) * np.sum(galaxy[1] > expands1),
            ]
        )

    for i in range(len(expanded_galaxies)):
        for j in range(i):
            d = dist(expanded_galaxies[i], expanded_galaxies[j])
            # print(galaxies[i], galaxies[j], d)
            answer += d

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
