from __future__ import annotations

import logging
import fire
import numpy as np
from adventofcode.helper.io import get_day, get_riddle_input, save_riddle_input


EXAMPLE = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""


def riddle1(riddle_input: str) -> int | str:
    answer = 0

    bucket = []
    matrices = []
    for i, line in enumerate(riddle_input.splitlines()):
        if line != "":
            bucket.append([_ == "#" for _ in line])
        else:
            matrix = np.array(bucket, dtype=int)
            bucket = []
            matrices.append(matrix)
    matrices.append(np.array(bucket, dtype=int))

    for matrix in matrices:
        # print(matrix)
        for colid in np.arange(0.5, matrix.shape[1] - 0.5, 1):
            # print(colid, matrix.shape[1])
            # print(rowid)
            left = np.arange(0, colid, step=1, dtype=int)
            right = np.arange(colid + 0.5, matrix.shape[1], step=1, dtype=int)
            n = min(len(left), len(right))
            # print(left, right, matrix.shape[0])
            left = left[-n:].flatten()
            right = right[:n].flatten()

            # print(left, right, matrix.shape[0])

            if np.all(matrix[:, left[::-1]] == matrix[:, right]):
                # print(matrix)
                # print("col", int(colid + 0.5))
                answer += int(colid + 0.5)
        for rowid in np.arange(0.5, matrix.shape[0] - 0.5, 1):
            # print(colid, matrix.shape[1])
            # print(rowid)
            above = np.arange(0, rowid, step=1, dtype=int)
            below = np.arange(rowid + 0.5, matrix.shape[0], step=1, dtype=int)
            n = min(len(above), len(below))
            # print(left, right, matrix.shape[0])
            above = above[-n:].flatten()
            below = below[:n].flatten()

            # print(left, right, matrix.shape[0])

            if np.all(matrix[above[::-1], :] == matrix[below, :]):
                # print(matrix)
                # print("row", int(rowid + 0.5))
                answer += 100 * int(rowid + 0.5)
        # for colid in range(matrix.shape[1]):

    return answer


def riddle2(riddle_input: str) -> int | str:
    answer = 0

    bucket = []
    matrices = []
    for i, line in enumerate(riddle_input.splitlines()):
        if line != "":
            bucket.append([_ == "#" for _ in line])
        else:
            matrix = np.array(bucket, dtype=int)
            bucket = []
            matrices.append(matrix)
    matrices.append(np.array(bucket, dtype=int))

    for matrix in matrices:
        # print(matrix)
        for colid in np.arange(0.5, matrix.shape[1] - 0.5, 1):
            # print(colid, matrix.shape[1])
            # print(rowid)
            left = np.arange(0, colid, step=1, dtype=int)
            right = np.arange(colid + 0.5, matrix.shape[1], step=1, dtype=int)
            n = min(len(left), len(right))
            # print(left, right, matrix.shape[0])
            left = left[-n:].flatten()
            right = right[:n].flatten()

            # print(left, right, matrix.shape[0])

            if np.sum(np.abs(matrix[:, left[::-1]] - matrix[:, right])) == 1:
                # print(matrix)
                # print("col", int(colid + 0.5))
                answer += int(colid + 0.5)
        for rowid in np.arange(0.5, matrix.shape[0] - 0.5, 1):
            # print(colid, matrix.shape[1])
            # print(rowid)
            above = np.arange(0, rowid, step=1, dtype=int)
            below = np.arange(rowid + 0.5, matrix.shape[0], step=1, dtype=int)
            n = min(len(above), len(below))
            # print(left, right, matrix.shape[0])
            above = above[-n:].flatten()
            below = below[:n].flatten()

            # print(left, right, matrix.shape[0])

            if np.sum(np.abs(matrix[above[::-1], :] - matrix[below, :])) == 1:
                # print(matrix)
                # print("row", int(rowid + 0.5))
                answer += 100 * int(rowid + 0.5)
        # for colid in range(matrix.shape[1]):

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


if __name__ == "__main__":
    fire.Fire(aoc)
