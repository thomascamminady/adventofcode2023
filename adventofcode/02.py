from __future__ import annotations

from rich import print

from adventofcode.helper.io import get_day, get_riddle_input, save_riddle_input


def riddle1(riddle_input: str) -> int | str:
    answer = 0
    boxes = {"red": 12, "green": 13, "blue": 14}

    def f(games):
        for game in games.split(";"):
            inventory = {}
            for numbercolor in game.split(","):
                number, color = numbercolor.strip().split(" ")
                inventory[color] = int(number)
            for color, count in inventory.items():
                if count > boxes[color]:
                    # print(f"games {i} not possible:{games}")
                    return 0
        else:
            return i + 1

    for i, line in enumerate(riddle_input.splitlines()):
        games = line.split(":")[-1]
        answer += f(games)

    return answer


def riddle2(riddle_input: str) -> int | str:
    answer = 0
    for i, line in enumerate(riddle_input.splitlines()):
        games = line.split(":")[-1]
        inventories = []
        for game in games.split(";"):
            inventory = {}
            for numbercolor in game.split(","):
                number, color = numbercolor.strip().split(" ")
                inventory[color] = int(number)
            inventories.append(inventory)

        boxes = {"red": 0, "green": 0, "blue": 0}
        for inventory in inventories:
            for color, value in inventory.items():
                boxes[color] = max(boxes[color], value)

        power = boxes["red"] * boxes["blue"] * boxes["green"]
        answer += power

    return answer


if __name__ == "__main__":
    day = get_day(__file__)
    riddle_input = get_riddle_input(day)
    save_riddle_input(day, riddle_input)

    #     # placeholder for example
    #     riddle_input = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    # Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    # Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    # Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    # Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

    # print(riddle_input)
    answer1 = riddle1(riddle_input)
    print(answer1)

    if answer1 != 0:
        answer2 = riddle2(riddle_input)
        print(answer2)
