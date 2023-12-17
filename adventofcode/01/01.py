from __future__ import annotations

from rich import print

from adventofcode.helper.io import get_day, get_riddle_input, save_riddle_input


def riddle1(riddle_input: str) -> int | str:
    answer = 0

    for i, line in enumerate(riddle_input.splitlines()):
        first = None
        last = None
        for char in line:
            if char in [str(i) for i in range(1, 10)]:
                last = int(char)
                if first is None:
                    first = int(char)
        if first is None or last is None:
            raise ValueError

        answer += first * 10 + last
        pass

    return answer


def find_first_word_in_line(line: str) -> tuple[int | None, str | None, str | None]:
    first = None
    first_word = None
    first_word_replace_with = None
    for i, word in enumerate(
        [
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
        ]
    ):
        position = line.find(word)
        if position >= 0:
            if first is None or position <= first:
                first = position
                first_word = word
                first_word_replace_with = str(i + 1)
    return first, first_word, first_word_replace_with


def modify(line: str) -> str:
    while True:
        first, first_word, first_word_replace_with = find_first_word_in_line(line)
        if first is None or first_word is None or first_word_replace_with is None:
            return line
        line = line.replace(first_word[:-1], first_word_replace_with)


def riddle2(riddle_input: str) -> int | str:
    answer = 0

    for _, line in enumerate(riddle_input.splitlines()):
        first = None
        last = None
        for char in modify(line):
            if char in [str(i) for i in range(0, 10)]:
                if first is None:
                    first = int(char)
                last = int(char)

        if first is None or last is None:
            raise ValueError

        answer += first * 10 + last
        pass

    return answer


if __name__ == "__main__":
    day = get_day(__file__)
    riddle_input = get_riddle_input(day)
    save_riddle_input(day, riddle_input)

    answer1 = riddle1(riddle_input)
    print(answer1)

    if answer1 != 0:
        answer2 = riddle2(riddle_input)
        print(answer2)
