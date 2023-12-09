from __future__ import annotations

import fire
from adventofcode.helper.io import get_day, get_riddle_input, save_riddle_input
import networkx as nx
import matplotlib.pyplot as plt
import logging


def print(_):
    logging.info(_)


def parse(riddle_input):
    successors = {}
    instructions = None
    for i, line in enumerate(riddle_input.splitlines()):
        if i == 0:
            instructions = line
        elif i == 1:
            continue
        else:
            center = line.split("=")[0].strip()
            left, right = line.split("=")[1].split(",")
            left = left.replace("(", "").strip()
            right = right.replace(")", "").strip()

            successors[center] = (left, right)
    return instructions, successors


def riddle1(riddle_input: str) -> int | str:
    instructions, successors = parse(riddle_input)
    start = "AAA"
    assert instructions is not None
    counter = 0
    while start != "ZZZ":
        if instructions[counter % len(instructions)] == "L":
            start = successors[start][0]
        else:
            start = successors[start][1]
        counter += 1
    return counter


def get_weakly_connected_subgraphs(graph):
    wcc_subgraphs = []
    # for wcc in nx.connected_components(graph):
    for wcc in nx.weakly_connected_components(graph):
        wcc_subgraph = graph.subgraph(wcc).copy()
        wcc_subgraphs.append(wcc_subgraph)
    return wcc_subgraphs


def riddle2(riddle_input: str) -> int | str:
    G = nx.DiGraph()

    succesors = {}
    instructions = None
    for i, line in enumerate(riddle_input.splitlines()):
        if i == 0:
            instructions = line
        if i < 2:
            continue
        center = line.split("=")[0].strip()
        left, right = line.split("=")[1].split(",")
        left = left.replace("(", "").strip()
        right = right.replace(")", "").strip()
        succesors[center] = (left, right)
        G.add_edges_from([(center, left), (center, right)])
    assert instructions is not None

    wcc_Subgraphs = get_weakly_connected_subgraphs(G)
    plt.close("all")
    for _ in wcc_Subgraphs:
        fig, ax = plt.subplots()
        color_map = []
        for node in _:
            if node[2] == "Z":
                color_map.append("blue")
            elif node[2] == "A":
                color_map.append("green")
            else:
                color_map.append("gray")
        nx.draw(
            _, node_color=color_map, with_labels=True, pos=nx.kamada_kawai_layout(_)
        )
        # plt.show()
        # nx.draw_networkx(_)
    plt.show()

    summary = []
    for subgraph in wcc_Subgraphs:
        # print("/")
        # print(g.nodes())
        # print([_ for _ in subgraph.nodes() if _[2] == "A"])
        # print([_ for _ in subgraph.nodes() if _[2] == "Z"])
        la = [_ for _ in subgraph.nodes() if _[2] == "A"][0]
        lz = [_ for _ in subgraph.nodes() if _[2] == "Z"][0]
        sp = nx.shortest_path_length(subgraph, la, lz)
        summary.append((la, lz, sp))
        print((la, lz, sp))
    # print(summary)

    periods = [s[2] for s in summary]
    period = 1
    for v in periods:
        period *= v
    print(period)

    starts = [_ for _ in succesors.keys() if _[2] == "A"]
    counters = []
    print(starts)
    for start in starts:
        orig = start
        counter = 0
        while start[2] != "Z":
            if instructions[counter % len(instructions)] == "L":
                start = succesors[start][0]
            else:
                start = succesors[start][1]
            counter += 1
        print((orig, start, counter))
        counters.append(counter)
    # print(counters)
    from math import lcm

    print(lcm(*counters))

    for _ in range(1, 1_000):
        if instructions[_ * period % len(instructions)] == "R":
            return _ * period
    return -1


def aoc(
    show: bool = False, save: bool = True, example: bool = False, log: bool = False
):
    if log:
        logging.basicConfig(level=logging.INFO)

    day = get_day(__file__)
    riddle_input = get_riddle_input(day)
    example_riddle_input = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
    if save:
        save_riddle_input(day, riddle_input)
    if show:
        print(riddle_input)
    if example:
        riddle_input = example_riddle_input

    # answer1 = riddle1(riddle_input)
    # print(answer1)

    answer2 = riddle2(riddle_input)
    print(answer2)


if __name__ == "__main__":
    fire.Fire(aoc)
