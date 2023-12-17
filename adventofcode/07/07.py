from __future__ import annotations

from rich import print
import fire
from adventofcode.helper.io import get_day, get_riddle_input, save_riddle_input
from collections import Counter

EXAMPLE_RIDDLE_INPUT = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


def do_rank_orig(cards):
    c = Counter(cards)
    n = list(c.values())
    if max(n) == 5:
        return 1
    elif max(n) == 4:
        return 2
    elif 3 in n and 2 in n:
        return 3
    elif 3 in n:
        return 4
    elif n.count(2) == 2:
        return 5
    elif n.count(2) == 1:
        return 6
    else:
        return 7


def do_rank(cards):
    print(cards)
    if "J" not in cards:
        return cards, do_rank_orig(cards)
    replace = find_most_common_card(cards)
    # print(cards, replace)
    yy = cards.replace("J", replace)
    print("     ", yy)
    return yy, do_rank_orig(yy)


def find_most_common_card(hand):
    """
    Function to find the most frequently occurring card in the hand.
    In case of a tie, returns the card with the highest value.
    """
    card_count = Counter(hand)
    # if "J" in card_count:
    #     if card_count["J"] == 3:
    #         return "A"
    if "J" in card_count:
        if card_count["J"] == 5:
            return "A"
        card_count["J"] = 0
    # possibles = [
    #     l for l in card_count.items() if card_count[l] == max(card_count.values())
    # ]make git
    # poss_v = [get_single_value(o) for o in possibles]
    # print(card_count, poss_v, possibles)
    # for _ in possibles:
    #     if get_single_value(_) == max(poss_v):
    #         return _

    return max(card_count, key=lambda x: (card_count[x], int(get_single_value(x))))


def get_single_value(letter):
    d = "A,K,Q,T,9,8,7,6,5,4,3,2,J"
    for i, di in enumerate(d.split(",")):
        if letter == di:
            return str(16 - i)
    return "00"


def get_value(cards):
    value = ""

    for i, card in enumerate(cards):
        x = get_single_value(card)
        if len(x) == 1:
            x = "0" + x
        value += x

        # value += 16 ** (10 - i) * get_single_value(card)

    return int(value)


def assign_order(z):
    answer = 0
    counter = 0
    M = len(z)
    for k in range(1, 8):
        print()
        print(k)
        print()
        possible = [_ for _ in z if _["rank"] == k]
        if len(possible) == 1:
            answer += (M - counter) * possible[0]["bid"]
            counter += 1
            # print(possible[0]["cards"])
        else:
            values = [get_value(_["orig_cards"]) for _ in possible]
            import numpy as np

            ranks = np.argsort(-np.array(values)).tolist()
            ranks = np.argsort(np.argsort(-np.array(values))).tolist()

            # ranks = [i[0] for i in sorted(enumerate(values), key=lambda x: -x[1])]

            # print(values, ranks)
            # print(values)
            # print(ranks)
            # print(ranks)
            for req_rank in range(len(values)):
                for i in range(len(values)):
                    if ranks[i] == req_rank:
                        answer += (M - counter) * possible[i]["bid"]
                        counter += 1
                        print(
                            possible[i]["cards"],
                            "*",
                            values[i],
                            " ",
                            ranks[i],
                            " ",
                            possible[i]["orig_cards"],
                            "*",
                            end=",",
                        )
                        break

    return answer


def riddle1(riddle_input: str) -> int | str:
    z = []
    for i, line in enumerate(riddle_input.splitlines()):
        cards, bid = line.split()
        bid = int(bid)
        orig_cards = cards
        mod_cards, rank = do_rank(cards)
        z.append(
            {"cards": mod_cards, "rank": rank, "bid": bid, "orig_cards": orig_cards}
        )
    # print(z)
    print(z)
    return assign_order(z)


def riddle2(riddle_input: str) -> int | str:
    answer = 0

    for i, line in enumerate(riddle_input.splitlines()):
        pass

    return answer


def aoc(show: bool = False, save: bool = True, example: bool = False):
    day = get_day(__file__)
    riddle_input = get_riddle_input(day)
    if save:
        save_riddle_input(day, riddle_input)
    if example:
        riddle_input = EXAMPLE_RIDDLE_INPUT
    if show:
        print(riddle_input)

    answer1 = riddle1(riddle_input)
    print(answer1)

    if answer1 != 0:
        answer2 = riddle2(riddle_input)
        print(answer2)


if __name__ == "__main__":
    fire.Fire(aoc)
