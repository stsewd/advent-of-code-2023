import pytest
from pathlib import Path
from textwrap import dedent


def solve(text: str) -> int:
    matrix = text.splitlines()
    total = 0
    n = len(matrix)
    for j in range(len(matrix[0])):
        block = -1
        for i in range(len(matrix)):
            if matrix[i][j] == "O":
                block += 1
                total += n - block
            elif matrix[i][j] == "#":
                block = i

    return total


def main():
    text = Path("14.txt").read_text()
    print(solve(text))


if __name__ == "__main__":
    main()


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
    assert solve(text) == 136


def test_input():
    p = Path("14.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 109661
