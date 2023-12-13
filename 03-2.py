import pytest
from pathlib import Path
from textwrap import dedent


def get_adjacent_numbers(
    table: list[str], numbers: list[list[tuple[int, int]]], row: int, col: int
) -> tuple[int, int] | None:
    adjancent_numbers = set()
    left_limit = col
    right_limit = col

    # Check right
    if col < len(table[row]) - 1:
        for start, end in numbers[row]:
            if col + 1 == start:
                adjancent_numbers.add((row, start, end))
                break
        right_limit += 1

    # Check left
    if col > 0:
        for start, end in numbers[row]:
            if col - 1 == end:
                adjancent_numbers.add((row, start, end))
                break
        left_limit -= 1

    # Check up
    if row > 0:
        for i in range(left_limit, right_limit + 1):
            char = table[row - 1][i]
            if char.isdigit():
                for start, end in numbers[row - 1]:
                    if i >= start and i <= end:
                        adjancent_numbers.add((row - 1, start, end))
                        break

    # Check down
    if row < len(table) - 1:
        for i in range(left_limit, right_limit + 1):
            char = table[row + 1][i]
            if char.isdigit():
                for start, end in numbers[row + 1]:
                    if i >= start and i <= end:
                        adjancent_numbers.add((row + 1, start, end))
                        break

    if len(adjancent_numbers) == 2:
        result = [
            int(table[row][start : end + 1]) for row, start, end in adjancent_numbers
        ]
        return result[0], result[1]

    return None


def solve(text: str) -> int:
    table = text.splitlines()
    # Collect all numbers.
    numbers = [[] for _ in range(len(table))]
    for i, row in enumerate(table):
        number = ""
        for j, c in enumerate(row):
            if c.isdigit():
                number += c
                is_end = j == len(row) - 1
                if is_end:
                    numbers[i].append((j - len(number) + 1, j))
            elif number:
                numbers[i].append((j - len(number), j - 1))
                number = ""

    # Inspect each `*` symbol, and check if it has adjacent numbers.
    total = 0
    for i, row in enumerate(table):
        for j, c in enumerate(row):
            if c == "*":
                adjacent_numbers = get_adjacent_numbers(
                    table=table, numbers=numbers, row=i, col=j
                )
                if adjacent_numbers:
                    total += adjacent_numbers[0] * adjacent_numbers[1]

    return total


def main():
    text = Path("03.txt").read_text()
    print(solve(text))


if __name__ == "__main__":
    main()


def test():
    text = dedent(
        """
        467..114..
        ...*......
        ..35..633.
        ......#...
        617*......
        .....+.58.
        ..592.....
        ......755.
        ...$.*....
        .664.598..
        """
    ).strip()
    assert solve(text) == 467835


def test_input():
    p = Path("03.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 73646890
