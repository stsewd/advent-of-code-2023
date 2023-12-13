import pytest
from pathlib import Path
from textwrap import dedent


def find_middle(pattern: list[int]) -> int:
    for i in range(len(pattern) - 1):
        index = len(pattern) - i - 1
        start = index
        end = min((len(pattern) - index), index)
        for j in range(index, index + end):
            index -= 1
            if pattern[j] != pattern[index]:
                break
        else:
            return start
    return -1


def get_result(pattern: list[str]) -> int:
    vertical = []
    for j in range(len(pattern[0])):
        n = 0
        for i in range(len(pattern)):
            if pattern[i][j] == "#":
                n += 2**i
        vertical.append(n)

    index = find_middle(vertical)
    if index != -1:
        return index

    horizontal = []
    for i in range(len(pattern)):
        n = 0
        for j in range(len(pattern[0])):
            if pattern[i][j] == "#":
                n += 2**j
        horizontal.append(n)

    index = find_middle(horizontal)
    if index != -1:
        return index * 100

    return 0


def solve(text: str) -> int:
    total = 0
    for patter in text.split("\n\n"):
        total += get_result(patter.splitlines())

    return total


def main():
    text = Path("13.txt").read_text()
    print(solve(text))


if __name__ == "__main__":
    main()


def test():
    text = dedent(
        """
        #.##..##.
        ..#.##.#.
        ##......#
        ##......#
        ..#.##.#.
        ..##..##.
        #.#.##.#.

        #...##..#
        #....#..#
        ..##..###
        #####.##.
        #####.##.
        ..##..###
        #....#..#
        """
    ).strip()
    assert solve(text) == 405


def test_input():
    p = Path("13.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 29130
