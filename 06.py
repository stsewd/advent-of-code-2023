import sys
import pytest
from pathlib import Path
import math
from textwrap import dedent


def solve(text: str) -> int:
    lines = text.splitlines()
    times = list(map(int, lines[0].split(":", maxsplit=1)[1].split()))
    distances = list(map(int, lines[1].split(":", maxsplit=1)[1].split()))

    total = 1
    for i in range(len(times)):
        time = times[i]
        distance = distances[i]
        i = math.ceil((time - math.sqrt((time**2) - (4 * distance))) / 2)
        if (i * (time - i)) <= distance:
            i += 1

        max_peek = (time - 1) // 2
        if time % 2 == 0:
            max_peek += 1
        if i < max_peek:
            if time % 2 == 0:
                subtotal = (max_peek - i) * 2 + 1
            else:
                subtotal = (max_peek - i + 1) * 2
            total *= subtotal
    return total


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
    assert solve(text) == 288


def test_input():
    p = Path("06.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 3317888
