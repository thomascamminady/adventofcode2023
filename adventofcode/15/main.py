from __future__ import annotations

import fire
from adventofcode.helper.io import (
    get_day,
    get_example_input,
    get_riddle_input,
    save_riddle_input,
)


def hash(string: str) -> int:
    h = 0
    for s in string:
        h += ord(s)
        h *= 17
        h %= 256
    return h


def riddle1(riddle_input: str) -> int | str:
    strings = [s.strip() for s in riddle_input.split(",")]

    return sum([hash(_) for _ in strings])


def riddle2(riddle_input: str) -> int | str:
    boxes2labels = {boxid: [] for boxid in range(256)}
    labels2lenses = {}
    for _, line in enumerate(riddle_input.split(",")):
        if "=" in line:
            label, focallength = line.split("=")
            boxid = hash(label)
            if label not in boxes2labels[boxid]:
                boxes2labels[boxid].append(label)
            labels2lenses[(boxid, label)] = focallength
        else:  # -
            label, focallength = line.split("-")
            boxid = hash(label)
            relevantbox = hash(label)
            if label in boxes2labels[relevantbox]:
                boxes2labels[relevantbox].remove(label)
                _ = labels2lenses.pop((relevantbox, label))

        # print()
        # print(hash(label))
        # print(line)
        # print(boxid)
        # for boxid, labels in boxes2labels.items():
        #     if labels != []:
        #         y = [labels2lenses[(boxid, labeli)] for labeli in labels]
        #         print(boxid, [(a, b) for a, b in zip(labels, y)])

        # print(boxes2labels)
        # print(labels2lenses)

    answer = 0
    for boxid, labels in boxes2labels.items():
        if labels != []:
            y = [labels2lenses[(boxid, labeli)] for labeli in labels]
            # yy = [(a, b) for a, b in zip(labels, y)]
            for j, focallength in enumerate(y):
                answer += (boxid + 1) * (j + 1) * int(focallength)

    return answer


def aoc(save: bool = True, show: bool = False, example: bool = False):
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
