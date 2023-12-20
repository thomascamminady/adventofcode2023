from __future__ import annotations
from abc import ABC, abstractmethod

import fire
from adventofcode.helper.io import (
    get_day,
    get_example_input,
    get_riddle_input,
    save_riddle_input,
)
from rich import print


class Module(ABC):
    def __init__(self, name: str, connections: list[str]) -> None:
        self.name = name
        self.connections = connections
        self.on = False

    @abstractmethod
    def receives(self, source: str, high_pulse: bool) -> list[tuple[str, str, bool]]:
        pass


class Broadcast(Module):
    def receives(self, source: str, high_pulse: bool) -> list[tuple[str, str, bool]]:
        return [(self.name, _, high_pulse) for _ in self.connections]


class Conjunction(Module):
    def __init__(self, name: str, connections: list[str]) -> None:
        self.remembers_high = [False for _ in connections]
        super().__init__(name, connections)

    def receives(self, source: str, high_pulse: bool) -> list[tuple[str, str, bool]]:
        for i in range(len(self.connections)):
            if self.connections[i] == source:
                self.remembers_high[i] = high_pulse

        if all(self.remembers_high):
            return [(self.name, _, False) for _ in self.connections]
        else:
            return [(self.name, _, True) for _ in self.connections]


class FlipFlop(Module):
    def receives(self, source: str, high_pulse: bool) -> list[tuple[str, str, bool]]:
        if not high_pulse:
            self.state = not self.state
            return [(self.name, _, self.state) for _ in self.connections]
        return []


class ModuleFactory:
    def __init__(self) -> None:
        pass

    def create(self, line) -> Module:
        sign = line[0].strip()
        name, connections = line[1:].split("->")
        name = name.strip()
        connections = [_.strip() for _ in connections.split(",")]
        print(line, name, connections)
        if sign == "b":
            return Broadcast("broadcaster", connections)
        elif sign == "%":
            return FlipFlop(name, connections)
        elif sign == "&":
            return Conjunction(name, connections)
        else:
            raise ValueError


def parse(riddle_input: str) -> dict[str, Module]:
    mf = ModuleFactory()
    modules = {}
    for i, line in enumerate(riddle_input.splitlines()):
        module = mf.create(line)
        modules[module.name] = module
    return modules


def riddle1(riddle_input: str) -> int | str:
    answer = 0
    modules = parse(riddle_input)
    print(modules)
    stack: list[tuple[str, str, bool]] = [("god", "broadcaster", True)]
    while len(stack) > 0:
        source, target, pulse = stack.pop(0)

        outcome = modules[target].receives(source, pulse)
        print(outcome)
        stack.extend(outcome)
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
