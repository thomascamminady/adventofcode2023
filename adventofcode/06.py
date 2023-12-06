from __future__ import annotations

from rich import print
import fire
from adventofcode.helper.io import get_day, get_riddle_input, save_riddle_input


def riddle1(riddle_input: str) -> int | str:
    answer = 1

    time = [int(_) for _ in riddle_input.splitlines()[0].split(":")[1].split()]
    dist = [int(_) for _ in riddle_input.splitlines()[1].split(":")[1].split()]

    for ti, di in zip(time, dist):
        print(ti, di)
        answeri = 0
        for charging_time in range(ti):
            distance = charging_time * (ti - charging_time)
            if distance > di:
                answeri += 1
        answer *= answeri

    return answer


def riddle2(riddle_input: str) -> int | str:
    answer = 0

    time = [int(_) for _ in riddle_input.splitlines()[0].split(":")[1].split()]
    dist = [int(_) for _ in riddle_input.splitlines()[1].split(":")[1].split()]
    time = int("".join([str(_) for _ in time]))
    dist = int("".join([str(_) for _ in dist]))
    print(time, dist)
    for i, charging_time in enumerate(range(time)):
        if i % 1_000_000 == 0:
            print(i)
        distance = charging_time * (time - charging_time)
        if distance > dist:
            answer += 1

    return answer


def aoc(show: bool = False, save: bool = True, example: bool = False):
    day = get_day(__file__)
    riddle_input = get_riddle_input(day)
    # placeholder for example
    example_riddle_input = """Time:      7  15   30
    Distance:  9  40  200
    """
    if save:
        save_riddle_input(day, riddle_input)
    if show:
        print(riddle_input)
    if example:
        riddle_input = example_riddle_input

    answer1 = riddle1(riddle_input)
    print(answer1)

    if answer1 != 0:
        answer2 = riddle2(riddle_input)
        print(answer2)


if __name__ == "__main__":
    fire.Fire(aoc)
