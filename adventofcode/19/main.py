from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Literal

import fire
from adventofcode.helper.io import (
    get_day,
    get_example_input,
    get_riddle_input,
    save_riddle_input,
)

from rich import print


@dataclass
class Instruction:
    field: str
    op: Literal["<", ">"]
    value: int
    reroute: str


def parse(riddle_input) -> tuple[dict[Any, Any], list[Any]]:
    workflows = {}
    firsthalf = True
    items = []
    for i, line in enumerate(riddle_input.splitlines()):
        if line == "":
            firsthalf = False
            continue

        if firsthalf:
            name, remainder = line.split("{")
            remainder = remainder[:-1]
            otherwise = remainder.split(",")[-1]
            instructions = ",".join(remainder.split(",")[:-1])
            instructions = instructions.split(",")
            instructions = [
                Instruction(
                    _.split(":")[0][0],
                    _.split(":")[0][1],
                    int(_.split(":")[0][2:]),
                    _.split(":")[1],
                )
                for _ in instructions
            ]
            workflows[name] = (instructions, otherwise)
        if not firsthalf:
            tmp = {}
            line = line[1:-1]
            for _ in line.split(","):
                a, b = _.split("=")
                tmp[a] = int(b)
            items.append(tmp)

    return workflows, items


def apply_workflows(
    workflows: dict[str, tuple[list[Instruction], str]], item: dict, current: str
) -> bool:
    instructions, otherwise = workflows[current]
    print(current)
    for ins in instructions:
        print(ins)
        if ins.op == ">":
            win = item[ins.field] > ins.value
        else:
            win = item[ins.field] < ins.value
        print(win)
        if win:
            if item[ins.field] > ins.value:
                if ins.reroute == "A":
                    return True
                elif ins.reroute == "R":
                    return False
                else:
                    return apply_workflows(workflows, item, ins.reroute)

    print(otherwise)
    if otherwise == "A":
        return True
    elif otherwise == "R":
        return False
    else:
        return apply_workflows(workflows, item, otherwise)


def riddle1(riddle_input: str) -> int | str:
    answer = 0

    workflows, items = parse(riddle_input)
    print(items)
    for item in items:
        print(" ")
        print(" ")
        print(item)

        y = apply_workflows(workflows, item, "in")

        print("result: ", y)
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
