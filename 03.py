import sys
import pytest
from pathlib import Path
from textwrap import dedent


def has_adjacent_symbol(table: list[str], row: int, start: int, end: int) -> bool:
    # Check right
    if end < len(table[row]) - 1:
        end += 1
        if table[row][end] != ".":
            return True

    # Check left
    if start > 0:
        start -= 1
        if table[row][start] != ".":
            return True

    # Check up
    if row > 0:
        for i in range(start, end + 1):
            char = table[row - 1][i]
            if char != "." and not char.isdigit():
                return True

    # Check down
    if row < len(table) - 1:
        for i in range(start, end + 1):
            char = table[row + 1][i]
            if char != "." and not char.isdigit():
                return True

    return False


def solve(text: str) -> int:
    table = text.splitlines()
    total = 0
    for i, row in enumerate(table):
        number = ""
        for j, c in enumerate(row):
            if c.isdigit():
                # Collect all digits.
                number += c
                # If we're at the end of the row,
                # check if we have an adjacent symbol.
                is_end = j == len(row) - 1
                if is_end and has_adjacent_symbol(
                    table=table,
                    row=i,
                    start=j - len(number) + 1,
                    end=j,
                ):
                    total += int(number)
            # If we're at a symbol, and we have a number,
            # check if we have an adjacent symbol.
            elif number:
                if has_adjacent_symbol(
                    table=table,
                    row=i,
                    start=j - len(number),
                    end=j - 1,
                ):
                    total += int(number)
                number = ""
    return total


if __name__ == "__main__":
    p = Path(sys.argv[1])
    print(solve(p.read_text()))


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
    assert solve(text) == 4361


def test_input():
    p = Path("03.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 531932
