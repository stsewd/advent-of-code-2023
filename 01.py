from pathlib import Path
import pytest
from textwrap import dedent


def solve(text: str) -> int:
    total = 0
    for line in text.splitlines():
        number = ""
        for c in line:
            if c.isdigit():
                number += c
                break

        for c in reversed(line):
            if c.isdigit():
                number += c
                break

        total += int(number)
    return total


def main():
    input_text = Path("01.txt").read_text()
    print(solve(input_text))


if __name__ == "__main__":
    main()


def test():
    text = dedent(
        """
        1abc2
        pqr3stu8vwx
        a1b2c3d4e5f
        treb7uchet
        """
    ).strip()
    assert solve(text) == 142


def test_input():
    p = Path("01.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 53334
