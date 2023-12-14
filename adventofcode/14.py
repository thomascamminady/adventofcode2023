from __future__ import annotations

import logging
import fire
from adventofcode.helper.io import get_day, get_riddle_input, save_riddle_input
import numpy as np

EXAMPLE = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


def tilt_north(M):
    for i in range(1, M.shape[0]):
        for j in range(M.shape[1]):
            if M[i, j] == "O":
                # stone that can move
                newpos = i
                while True:
                    if newpos == 0:
                        break
                    if M[newpos - 1, j] == ".":
                        newpos -= 1
                    else:
                        break
                M[i, j] = "."
                M[newpos, j] = "O"
    return M


def riddle1(riddle_input: str) -> int | str:
    answer = 0
    M = np.array([[_ for _ in line] for line in riddle_input.splitlines()], dtype=str)
    M = tilt_north(M)

    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if M[i, j] == "O":
                answer += M.shape[0] - i
    return answer


def riddle2(riddle_input: str) -> int | str:
    answer = 0

    M = np.array([[_ for _ in line] for line in riddle_input.splitlines()], dtype=str)

    previous_matrices = [M.copy()]

    def loop(M):
        for _ in range(1000000000):
            if (_ % (1000000000 // 1000)) == 0:
                print(_)
            print("iteration:", _)
            M = tilt_north(M)
            M = tilt_north(np.rot90(M, k=-1))
            M = tilt_north(np.rot90(M, k=-1))
            M = tilt_north(np.rot90(M, k=-1))
            M = np.rot90(M, k=-1)
            for j, pM in enumerate(previous_matrices):
                if np.all(pM == M):
                    print(_, j)
                    # print(previous_matrices)
                    return _, j, _ - j
            else:
                previous_matrices.append(M.copy())
        # print(" ")

    iteration, equal_to, cycle = loop(M)
    # 9 == 3
    print("reduced ", (1000000000 + 1 - (iteration + 1)) % cycle)
    # 3 == 9 == 9+6=15

    print(iteration, equal_to, cycle)
    print(((1000000001 - iteration) % cycle))
    for _ in range(cycle + 1):
        M = tilt_north(M)
        M = tilt_north(np.rot90(M, k=-1))
        M = tilt_north(np.rot90(M, k=-1))
        M = tilt_north(np.rot90(M, k=-1))
        M = np.rot90(M, k=-1)
        answer = 0
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                if M[i, j] == "O":
                    answer += M.shape[0] - i
        if _ == ((1000000001 - iteration) % cycle):
            print("next one:")
        print(answer)
    return answer


# 104788 too low


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
