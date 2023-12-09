from __future__ import annotations

import logging
import fire
from adventofcode.helper.io import get_day, get_riddle_input, save_riddle_input


EXAMPLE = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def diff(seq: list[int]) -> list[int]:
    return [seq[i] - seq[i - 1] for i in range(1, len(seq))]


def allzero(seq):
    for _ in seq:
        if _ != 0:
            return False
    return True


def riddle1(riddle_input: str) -> int | str:
    answer = 0

    for i, line in enumerate(riddle_input.splitlines()):
        orig = [int(_) for _ in line.split()]
        values = [int(_) for _ in line.split()]

        last_elements = []
        print(values)
        while not allzero(values):
            last_elements.append(values[-1])
            values = diff(values)
            # print(values)
        answer += sum(last_elements)

    return answer


def riddle2(riddle_input: str) -> int | str:
    answer = 0

    for i, line in enumerate(riddle_input.splitlines()):
        orig = [int(_) for _ in line.split()]
        values = [int(_) for _ in line.split()][::-1]

        last_elements = []
        print(values)
        while not allzero(values):
            last_elements.append(values[-1])
            values = diff(values)
            # print(values)
        answer += sum(last_elements)

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


def print(_):
    logging.info(_)


if __name__ == "__main__":
    fire.Fire(aoc)
