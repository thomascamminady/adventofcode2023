from __future__ import annotations

from rich import print
import fire
from adventofcode.helper.io import get_day, get_riddle_input, save_riddle_input
from numba import njit
import time


def riddle1(riddle_input: str) -> int | str:
    seeds = [int(_) for _ in riddle_input.splitlines()[0].split(":")[1].split()]

    list_of_mappings = []
    mapping_a_to_b = []
    for i, line in enumerate(riddle_input.splitlines()):
        if i == 0:
            continue
        elif "map" in line:
            mapping_a_to_b = []
        elif line == "":
            if mapping_a_to_b != []:
                list_of_mappings.append(mapping_a_to_b)
        else:
            dst = int(line.split()[0])
            src = int(line.split()[1])
            rng = int(line.split()[2])
            mapping_a_to_b.append((dst, src, rng))
    else:
        list_of_mappings.append(mapping_a_to_b)

    def apply_mapping(x, mapping_a_to_b):
        for dst, src, rng in mapping_a_to_b:
            if src <= x < src + rng:
                return dst + (x - src)
        else:
            return x

    def apply_mappings(x, list_of_mappings):
        for mapping_a_to_b in list_of_mappings:
            x = apply_mapping(x, mapping_a_to_b)
        return x

    locations = [apply_mappings(_, list_of_mappings) for _ in seeds]
    return min(locations)


def riddle2(riddle_input: str) -> int | str:
    seeds = [int(_) for _ in riddle_input.splitlines()[0].split(":")[1].split()]

    list_of_mappings = []
    mapping_a_to_b = []
    for i, line in enumerate(riddle_input.splitlines()):
        if i == 0:
            continue
        elif "map" in line:
            mapping_a_to_b = []
        elif line == "":
            if mapping_a_to_b != []:
                list_of_mappings.append(mapping_a_to_b)
        else:
            dst = int(line.split()[0])
            src = int(line.split()[1])
            rng = int(line.split()[2])
            mapping_a_to_b.append((dst, src, rng))
    else:
        list_of_mappings.append(mapping_a_to_b)

    def apply_mapping(x: int, mapping_a_to_b: list[tuple[int, int, int]]):
        for dst, src, rng in mapping_a_to_b:
            if src <= x < src + rng:
                return dst + (x - src)
        else:
            return x

    def apply_mappings(x: int, list_of_mappings: list[list[tuple[int, int, int]]]):
        for mapping_a_to_b in list_of_mappings:
            x = apply_mapping(x, mapping_a_to_b)
        return x

    for start, _range in zip(seeds[0::2], seeds[1::2]):
        left = start
        right = start + _range - 1


def aoc(show: bool = False, save: bool = True):
    day = get_day(__file__)
    riddle_input = get_riddle_input(day)
    if save:
        save_riddle_input(day, riddle_input)
    # placeholder for example
    riddle_input2 = """seeds: 79 14 55 13

    seed-to-soil map:
    50 98 2
    52 50 48

    soil-to-fertilizer map:
    0 15 37
    37 52 2
    39 0 15

    fertilizer-to-water map:
    49 53 8
    0 11 42
    42 0 7
    57 7 4

    water-to-light map:
    88 18 7
    18 25 70

    light-to-temperature map:
    45 77 23
    81 45 19
    68 64 13

    temperature-to-humidity map:
    0 69 1
    1 0 69

    humidity-to-location map:
    60 56 37
    56 93 4"""

    if show:
        print(riddle_input)

    answer1 = riddle1(riddle_input)
    print(answer1)

    if answer1 != 0:
        answer2 = riddle2(riddle_input)
        print(answer2)


if __name__ == "__main__":
    fire.Fire(aoc)
