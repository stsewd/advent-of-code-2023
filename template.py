import sys
import pytest
from pathlib import Path
from textwrap import dedent


def solve(text: str) -> int:
    return 0


if __name__ == "__main__":
    p = Path(sys.argv[1])
    print(solve(p.read_text()))


def test():
    text = dedent(
        """
        """
    ).strip()
    assert solve(text) == 0


def test_input():
    p = Path("00.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 0
