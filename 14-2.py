import sys
import pytest
from pathlib import Path
from textwrap import dedent


def move_north(matrix: list[list[str]]):
    for j in range(len(matrix[0])):
        block = -1
        for i in range(len(matrix)):
            if matrix[i][j] == "O":
                block += 1
                matrix[i][j] = "."
                matrix[block][j] = "O"
            elif matrix[i][j] == "#":
                block = i


def move_west(matrix: list[list[str]]):
    for i in range(len(matrix)):
        block = -1
        for j in range(len(matrix[0])):
            if matrix[i][j] == "O":
                block += 1
                matrix[i][j] = "."
                matrix[i][block] = "O"
            elif matrix[i][j] == "#":
                block = j


def move_south(matrix: list[list[str]]):
    for j in range(len(matrix[0])):
        block = len(matrix)
        for i in range(len(matrix) - 1, -1, -1):
            if matrix[i][j] == "O":
                block -= 1
                matrix[i][j] = "."
                matrix[block][j] = "O"
            elif matrix[i][j] == "#":
                block = i


def move_east(matrix: list[list[str]]):
    for i in range(len(matrix)):
        block = len(matrix[0])
        for j in range(len(matrix[0]) - 1, -1, -1):
            if matrix[i][j] == "O":
                block -= 1
                matrix[i][j] = "."
                matrix[i][block] = "O"
            elif matrix[i][j] == "#":
                block = j


def get_value(matrix: list[list[str]]) -> int:
    total = 0
    n = len(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == "O":
                total += n - i
    return total


# This was manually calculated by analyzing the value after each cycle (200), and look for a pattern.
stable_after = {10: (2, 7), 100: (97, 18)}


def solve(text: str, n: int) -> int:
    matrix = [[c for c in line] for line in text.splitlines()]

    start, loop = stable_after[len(matrix)]

    if n <= start:
        cycles = n
    else:
        cycles = start + ((n - start - 1) % loop) + 1

    for _ in range(cycles):
        move_north(matrix)
        move_west(matrix)
        move_south(matrix)
        move_east(matrix)
    return get_value(matrix)


if __name__ == "__main__":
    p = Path(sys.argv[1])
    print(solve(p.read_text(), n=1000000000))


def test():
    text = dedent(
        """
        O....#....
        O.OO#....#
        .....##...
        OO.#O....O
        .O.....O#.
        O.#..O.#.#
        ..O..#O..O
        .......O..
        #....###..
        #OO..#....
        """
    ).strip()
    assert solve(text, n=1000000000) == 64


def test_input():
    p = Path("14.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text, n=1000000000) == 90176
