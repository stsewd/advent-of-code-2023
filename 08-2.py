import sys
import pytest
from pathlib import Path
import math
from textwrap import dedent


def solve(text: str) -> int:
    lines = text.splitlines()
    directions = lines[0]
    nodes = {}
    start_nodes = []
    for line in lines[2:]:
        node, _, neighbors = line.split(maxsplit=2)
        neighbors = neighbors[1:-1].split(", ")
        nodes[node] = neighbors
        if node.endswith("A"):
            start_nodes.append(node)

    z_indexes = []
    for start_node in start_nodes:
        current_node = start_node
        steps = 0
        direction_index = 0
        while not current_node.endswith("Z"):
            direction = 0 if directions[direction_index] == "L" else 1
            neighbors = nodes[current_node]
            current_node = neighbors[direction]
            direction_index = (direction_index + 1) % len(directions)
            steps += 1
        z_indexes.append(steps)

    return math.lcm(*z_indexes)


if __name__ == "__main__":
    p = Path(sys.argv[1])
    print(solve(p.read_text()))


def test():
    text = dedent(
        """
        LR

        11A = (11B, XXX)
        11B = (XXX, 11Z)
        11Z = (11B, XXX)
        22A = (22B, XXX)
        22B = (22C, 22C)
        22C = (22Z, 22Z)
        22Z = (22B, 22B)
        XXX = (XXX, XXX)
        """
    ).strip()
    assert solve(text) == 6


def test_input():
    p = Path("08.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 21165830176709
