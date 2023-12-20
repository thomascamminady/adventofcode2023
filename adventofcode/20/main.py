from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

import fire
from adventofcode.helper.io import (
    get_day,
    get_example_input,
    get_riddle_input,
    save_riddle_input,
)
from rich import print


@dataclass
class Signal:
    source: str
    target: str
    high_pulse: bool

    def __repr__(self) -> str:
        return (
            f"""{self.source} -{"high" if self.high_pulse else "low"}-> {self.target}"""
        )


class Module(ABC):
    def __init__(self, name: str, connections: list[str]) -> None:
        self.name = name
        self.connections = connections
        self.on = False

    def receives(self, source: str, high_pulse: bool) -> list[Signal]:
        outcome = self._receives(source, high_pulse)
        return outcome

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def _receives(self, source: str, high_pulse: bool) -> list[Signal]:
        pass

    def __repr__(self) -> str:
        return f"{self.name}: state: {self.on}, conn:{self.connections},{type(self)}"


class Broadcast(Module):
    def _receives(self, source: str, high_pulse: bool) -> list[Signal]:
        return [Signal(self.name, _, high_pulse) for _ in self.connections]

    def reset(self) -> None:
        pass


class Conjunction(Module):
    def __init__(self, name: str, connections: list[str]) -> None:
        self.inputs = []
        self.remembers_high = []

        super().__init__(name, connections)

    def reset(self) -> None:
        self.remembers_high = [False for _ in self.remembers_high]

    def initialize_inputs(self, inputs: list[str]):
        self.inputs = inputs
        self.remembers_high = [False for _ in self.inputs]

    def _receives(self, source: str, high_pulse: bool) -> list[Signal]:
        idx = self.inputs.index(source)
        self.remembers_high[idx] = high_pulse

        if all(self.remembers_high):
            return [Signal(self.name, _, False) for _ in self.connections]
        else:
            return [Signal(self.name, _, True) for _ in self.connections]


class FlipFlop(Module):
    def reset(self) -> None:
        self.on = False

    def _receives(self, source: str, high_pulse: bool) -> list[Signal]:
        if not high_pulse:
            self.on = not self.on
            return [Signal(self.name, _, self.on) for _ in self.connections]
        return []


class ModuleFactory:
    def __init__(self) -> None:
        pass

    def create(self, line) -> Module:
        sign = line[0].strip()
        name, connections = line[1:].split("->")
        name = name.strip()
        connections = [_.strip() for _ in connections.split(",")]
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
    for name, module in modules.items():
        if isinstance(module, Conjunction):
            inputs = []
            for _name, _module in modules.items():
                if name in _module.connections:
                    inputs.append(_name)
            modules[name].initialize_inputs(inputs)
    return modules


def riddle1(riddle_input: str) -> int | str:
    modules = parse(riddle_input)
    number_high_pulses = 0
    number_low_pulses = 0
    for _ in range(1_000):
        # print(_)
        number_low_pulses += 1
        stack: list[Signal] = [Signal("button", "broadcaster", False)]
        while len(stack) > 0:
            # print(f"""stack:  {",   ".join([str(_) for _ in stack])}""")
            signal = stack.pop(0)
            if signal.target in modules.keys():
                outcome = modules[signal.target].receives(
                    signal.source, signal.high_pulse
                )
                for _ in outcome:
                    if _.high_pulse:
                        number_high_pulses += 1
                    else:
                        number_low_pulses += 1
                stack.extend(outcome)
    return number_high_pulses * number_low_pulses


def riddle2(riddle_input: str) -> int | str:
    modules = parse(riddle_input)
    number_high_pulses = 0
    number_low_pulses = 0
    print(modules)
    for _ in range(100000000):
        print(_)
        number_low_pulses += 1
        stack: list[Signal] = [Signal("button", "broadcaster", False)]
        while len(stack) > 0:
            # print(stack)
            # print(f"""stack:  {",   ".join([str(_) for _ in stack])}""")
            signal = stack.pop(0)
            if signal.target in modules.keys():
                outcome = modules[signal.target].receives(
                    signal.source, signal.high_pulse
                )
                for _ in outcome:
                    if _.high_pulse:
                        number_high_pulses += 1
                    else:
                        number_low_pulses += 1
                stack.extend(outcome)
            elif signal.target == "rx" and not signal.high_pulse:
                for key in modules.keys():
                    modules[key].reset()
                print(
                    number_high_pulses,
                    number_low_pulses,
                    number_high_pulses + number_low_pulses,
                )
                break
                number_high_pulses = 0
                number_low_pulses = 0
            # else:
            #     print(signal)
    return number_high_pulses * number_low_pulses


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
