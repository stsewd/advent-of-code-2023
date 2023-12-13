import pytest
from textwrap import dedent
from pathlib import Path
from functools import cmp_to_key
from collections import Counter

FIVE_OF_A_KIND = 7
FOUR_OF_A_KIND = 6
FULL_HOUSE = 5
THREE_OF_A_KIND = 4
TWO_PAIR = 3
ONE_PAIR = 2
HIGH_CARD = 1

CARDS = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
}


def get_hand_type(hand):
    if not hand:
        return HIGH_CARD

    counter = Counter(hand)

    most_common = [n for _, n in counter.most_common(2)]
    if len(most_common) == 1:
        most_common.append(0)

    if most_common[0] == 5:
        return FIVE_OF_A_KIND

    if most_common[0] == 4:
        return FOUR_OF_A_KIND

    if most_common[0] == 3:
        if most_common[1] == 2:
            return FULL_HOUSE
        return THREE_OF_A_KIND

    if most_common[0] == 2:
        if most_common[1] == 2:
            return TWO_PAIR
        return ONE_PAIR

    return HIGH_CARD


def get_hand_type_with_jokers(hand):
    hand_without_jokers = hand.replace("J", "")
    jokers = len(hand) - len(hand_without_jokers)

    hand_type = get_hand_type(hand_without_jokers)

    if not jokers:
        return hand_type

    if hand_type == FOUR_OF_A_KIND:
        return FIVE_OF_A_KIND

    if hand_type == THREE_OF_A_KIND:
        if jokers == 1:
            return FOUR_OF_A_KIND
        return FIVE_OF_A_KIND

    if hand_type == TWO_PAIR:
        return FULL_HOUSE

    if hand_type == ONE_PAIR:
        if jokers == 1:
            return THREE_OF_A_KIND
        if jokers == 2:
            return FOUR_OF_A_KIND
        return FIVE_OF_A_KIND

    if jokers == 1:
        return ONE_PAIR
    if jokers == 2:
        return THREE_OF_A_KIND
    if jokers == 3:
        return FOUR_OF_A_KIND
    return FIVE_OF_A_KIND


def cmp(a, b):
    a = a[0]
    b = b[0]
    a_type = get_hand_type_with_jokers(a)
    b_type = get_hand_type_with_jokers(b)

    if a_type != b_type:
        return a_type - b_type

    for card_a, card_b in zip(a, b):
        card_a = CARDS[card_a]
        card_b = CARDS[card_b]
        if card_a != card_b:
            return card_a - card_b

    return 0


def solve(text: str) -> int:
    cards = [line.split() for line in text.splitlines()]
    cards = sorted(cards, key=cmp_to_key(cmp))
    total = 0
    for i, hand in enumerate(cards):
        total += (i + 1) * int(hand[1])
    return total


def main():
    text = Path("07.txt").read_text()
    print(solve(text))


if __name__ == "__main__":
    main()


def test():
    text = dedent(
        """
        32T3K 765
        T55J5 684
        KK677 28
        KTJJT 220
        QQQJA 483
        """
    ).strip()
    assert solve(text) == 5905


def test_input():
    p = Path("07.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 251824095
