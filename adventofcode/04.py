from __future__ import annotations
from collections import defaultdict

from rich import print
import fire
from adventofcode.helper.io import get_day, get_riddle_input, save_riddle_input


def riddle1(riddle_input: str) -> int | str:
    answer = 0

    for i, line in enumerate(riddle_input.splitlines()):
        yours = [int(_) for _ in line.split(":")[1].split("|")[0].strip().split()]
        wins = [int(_) for _ in line.split(":")[1].split("|")[1].strip().split()]

        is_good = [1 if _ in wins else 0 for _ in yours]
        n = sum(is_good)
        if n == 0:
            answer += 0
        else:
            answer += 2 ** (n - 1)
    return answer


def riddle2(riddle_input: str) -> int | str:
    answer = 0

    def get_score(line):
        yours = [int(_) for _ in line.split(":")[1].split("|")[0].strip().split()]
        wins = [int(_) for _ in line.split(":")[1].split("|")[1].strip().split()]

        is_good = [1 if _ in wins else 0 for _ in yours]
        n = sum(is_good)
        return n

    wins = {i: get_score(line) for i, line in enumerate(riddle_input.splitlines())}
    inventory = defaultdict(int)
    for i in range(0, len(riddle_input.splitlines())):
        inventory[i] = 1
    active = 0
    original_inventory = {}
    while True:
        if inventory[active] == 0 and inventory[active + 1] == 0:
            break
        elif inventory[active] == 0:
            active += 1
        else:
            n = wins[active]
            original_inventory[active] = inventory[active]

            # print("here", n, inventory[active], active)
            for _ in range(n):
                inventory[active + _ + 1] += inventory[active]
            inventory[active] = 0
    return sum([v for k, v in original_inventory.items()])


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
        #         riddle_input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        # Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
        # Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
        # Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
        # Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
        # Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
        answer2 = riddle2(riddle_input)
        print(answer2)


if __name__ == "__main__":
    fire.Fire(aoc)
