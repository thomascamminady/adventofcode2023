from __future__ import annotations

import logging
import fire
from adventofcode.helper.io import get_day, get_riddle_input, save_riddle_input


EXAMPLE = """"""


def riddle1(riddle_input: str) -> int | str:
    answer = 0

    for i, line in enumerate(riddle_input.splitlines()):
        pass

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


if __name__ == "__main__":
    fire.Fire(aoc)
