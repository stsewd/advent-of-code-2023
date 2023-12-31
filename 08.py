import sys
import pytest
from pathlib import Path
from textwrap import dedent


def solve(text: str) -> int:
    lines = text.splitlines()
    directions = lines[0]
    nodes = {}
    for line in lines[2:]:
        node, _, neighbors = line.split(maxsplit=2)
        neighbors = neighbors[1:-1].split(", ")
        nodes[node] = neighbors

    current_node = "AAA"
    direction_index = 0
    total = 0
    while current_node != "ZZZ":
        neighbors = nodes[current_node]
        direction = 0 if directions[direction_index] == "L" else 1
        current_node = neighbors[direction]
        direction_index = (direction_index + 1) % len(directions)
        total += 1
    return total


if __name__ == "__main__":
    p = Path(sys.argv[1])
    print(solve(p.read_text()))


def test():
    text = dedent(
        """
        RL

        AAA = (BBB, CCC)
        BBB = (DDD, EEE)
        CCC = (ZZZ, GGG)
        DDD = (DDD, DDD)
        EEE = (EEE, EEE)
        GGG = (GGG, GGG)
        ZZZ = (ZZZ, ZZZ)
        """
    ).strip()
    assert solve(text) == 2

    text = dedent(
        """
        LLR

        AAA = (BBB, BBB)
        BBB = (AAA, ZZZ)
        ZZZ = (ZZZ, ZZZ)
        """
    ).strip()
    assert solve(text) == 6


def test_input():
    p = Path("08.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 21409
