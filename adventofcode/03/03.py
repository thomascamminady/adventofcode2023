from __future__ import annotations

from rich import print
import fire
import numpy as np
from adventofcode.helper.io import get_day, get_riddle_input, save_riddle_input
import re


def extract_numbers_with_positions(text):
    # Regular expression to find numbers and their positions
    matches = re.finditer(r"\d+", text)
    result = [(int(match.group()), match.start()) for match in matches]
    return result


def is_special(c):
    if c == "." or c in [str(i) for i in range(10)]:
        return False
    return True


def is_okay(i, j):
    _max = 139
    if i < 0 or i > _max or j < 0 or j > _max:
        return False
    return True


def riddle1(riddle_input: str) -> int | str:
    answer = 0

    y = []
    z = []
    for i, line in enumerate(riddle_input.splitlines()):
        x = extract_numbers_with_positions(line)

        y.append(x)
        z.append([_ for _ in line])
    M = np.array(z, dtype=str)

    for row, dummy in enumerate(y):
        for number, position in dummy:
            k = len(str(number))

            surroundings = []
            left = (row, position - 1)
            right = (row, position + k)
            above = [(row - 1, _) for _ in range(position - 1, position + k + 1)]
            below = [(row + 1, _) for _ in range(position - 1, position + k + 1)]
            surroundings.append(left)
            surroundings.append(right)
            surroundings.extend(above)
            surroundings.extend(below)
            found_any = False
            for s in surroundings:
                if is_okay(s[0], s[1]):
                    if is_special(M[s[0], s[1]]):
                        found_any = True

            if found_any:
                answer += int(number)

    return answer


def riddle2(riddle_input: str) -> int | str:
    answer = 0

    y = []
    z = []
    for i, line in enumerate(riddle_input.splitlines()):
        x = extract_numbers_with_positions(line)

        y.append(x)
        z.append([_ for _ in line])
    M = np.array(z, dtype=str)

    count = np.zeros((140, 140))
    first = np.zeros((140, 140))
    second = np.zeros((140, 140))

    for row, dummy in enumerate(y):
        for number, position in dummy:
            k = len(str(number))

            surroundings = []
            left = (row, position - 1)
            right = (row, position + k)
            above = [(row - 1, _) for _ in range(position - 1, position + k + 1)]
            below = [(row + 1, _) for _ in range(position - 1, position + k + 1)]
            surroundings.append(left)
            surroundings.append(right)
            surroundings.extend(above)
            surroundings.extend(below)
            for s in surroundings:
                i, j = s
                if is_okay(i, j):
                    if M[i, j] == "*":
                        count[i, j] += 1
                        if first[i, j] == 0:
                            first[i, j] = number
                        else:
                            second[i, j] = number

    return int(np.sum((count > 1) * first * second))

    return answer


def aoc(show: bool = False, save: bool = True):
    day = get_day(__file__)
    riddle_input = get_riddle_input(day)
    # placeholder for example
    # riddle_input = """"""
    if save:
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
