from __future__ import annotations

import logging
import fire
from adventofcode.helper.io import get_day, get_riddle_input, save_riddle_input

from itertools import product
from collections import Counter

EXAMPLE = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


def parse(line: str) -> tuple[list, list]:
    first, last = line.split()

    mapping = {"?": -1, ".": 0, "#": 1}
    digits = [mapping[_] for _ in first]
    counts = [int(_) for _ in last.split(",")]
    return digits, counts


def count(digits):
    c = []
    counter = 0
    for d in digits:
        if d == 1:
            counter += 1
        elif d == 0:
            if counter != 0:
                c.append(counter)
                counter = 0
        else:
            # print(digits)
            raise ValueError
    if digits[-1] == 1:
        c.append(counter)

    return c


def much_compute(line, cc) -> int:
    # line = ".??..??...?##."
    # counts = [1, 1, 3]
    counts = 5 * cc
    line = "?".join([line] * 5)
    s = [_ for _ in line.split(".") if _ != ""]
    # print(line)
    # print(s)
    # print(counts)
    all_possibilities = []
    for si in s:
        # print(si)
        mapping = {"?": -1, ".": 0, "#": 1}
        digits = [mapping[_] for _ in si]
        # print(digits)
        modify = [i for i, d in enumerate(digits) if d == -1]
        # print(modify)
        possibilities = []
        for modification in list(product([0, 1], repeat=len(modify))):
            x = [_ for _ in digits]
            for pos, val in zip(modify, modification):
                x[pos] = val
            _counts = count(x)
            if _counts == []:
                _counts = [None]
            possibilities.extend(_counts)
        # print("   ", possibilities)
        all_possibilities.append([(k, v) for k, v in Counter(possibilities).items()])

    all_possibilities_ids = [range(len(_)) for _ in all_possibilities]
    # print(all_possibilities)
    # print(all_possibilities_ids)
    import numpy as np

    answer = 0
    for i, x in enumerate(product(*all_possibilities_ids)):
        z = [_ for _ in x]
        _vals = [all_possibilities[pos][d][0] for pos, d in enumerate(z)]
        _cts = [all_possibilities[pos][d][1] for pos, d in enumerate(z)]
        _cts_reduced = [_ for _v, _ in zip(_vals, _cts) if _v is not None]
        _vals_reduced = [_ for _ in _vals if _ is not None]
        if _vals_reduced == counts:
            # print(i)
            # print(counts)
            # print(_vals)
            # print(z)
            # print(_cts)
            # print(_vals_reduced)
            # print(_cts_reduced)
            answer += np.prod(_cts_reduced)

        # if i > 10:
        #     break
    # print(answer, line, counts)
    return answer, line, counts


def riddle1(riddle_input: str) -> int | str:
    answer = 0

    for i, line in enumerate(riddle_input.splitlines()):
        counter = 0

        digits, counts = parse(line)
        # print(line, digits, counts)

        modify = [i for i, d in enumerate(digits) if d == -1]

        # print(line)
        for modification in list(product([0, 1], repeat=len(modify))):
            x = [_ for _ in digits]
            for pos, val in zip(modify, modification):
                x[pos] = val
            _counts = count(x)
            # print("    ", x, _counts)
            # print("...", modify, modification, x)
            if _counts == counts:
                counter += 1
        # print(line, counter)
        answer += counter
        print(i, counter)

    return answer


def riddle2(riddle_input: str) -> int | str:
    answer = 0

    for i, line in enumerate(riddle_input.splitlines()):
        digits, counts = parse(line)
        first, last = line.split(" ")
        cc = [int(_) for _ in last.split(",")]
        a, b, c = much_compute(first, cc)
        print(a, "                              ;", first, cc)
        print(b, c)
        answer += a

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

    """
    19 chars in total
    1,3,9,1 summed = 14
    5 spots HAVE TO BE .
    ?#????????????###?? 1,3,9,1 this implies there are at least 3 dots
    [.] = between 0 and inf many .
    (.) = between 1 and inf many .
    [.]1(.)[3](.)[9][.]
    expands to
    [.]#(.)###(.)#########[.]

    3 fold :
    ?#????????????###????#????????????###????#????????????###??
    1,3,9,1,1,3,9,1,1,3,9,1




    """
