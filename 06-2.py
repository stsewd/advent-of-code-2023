import sys
import pytest
import math
from pathlib import Path
from textwrap import dedent


def solve(text: str) -> int:
    lines = text.splitlines()
    time = int("".join(lines[0].split(":", maxsplit=1)[1].split()))
    distance = int("".join(lines[1].split(":", maxsplit=1)[1].split()))

    i = math.ceil((time - math.sqrt((time**2) - (4 * distance))) / 2)
    if (i * (time - i)) <= distance:
        i += 1

    max_peek = (time - 1) // 2
    if time % 2 == 0:
        max_peek += 1
    if i < max_peek:
        if time % 2 == 0:
            return (max_peek - i) * 2 + 1
        return (max_peek - i + 1) * 2
    return 0


if __name__ == "__main__":
    p = Path(sys.argv[1])
    print(solve(p.read_text()))


def test():
    text = dedent(
        """
        Time:      7
        Distance:  9
        """
    ).strip()
    assert solve(text) == 4

    text = dedent(
        """
        Time:      8
        Distance:  9
        """
    ).strip()
    assert solve(text) == 5

    text = dedent(
        """
        Time:      15
        Distance:  40
        """
    ).strip()
    assert solve(text) == 8

    text = dedent(
        """
        Time:      30
        Distance:  200
        """
    ).strip()
    assert solve(text) == 9
    text = dedent(
        """
        Time:      7  15   30
        Distance:  9  40  200
        """
    ).strip()
    assert solve(text) == 71503


def test_input():
    p = Path("06.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 24655068
