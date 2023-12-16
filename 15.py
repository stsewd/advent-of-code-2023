import sys
import pytest
from pathlib import Path
from textwrap import dedent


def solve(text: str) -> int:
    total = 0
    for word in text.strip().split(","):
        subtotal = 0
        for c in word:
            subtotal = ((subtotal + ord(c)) * 17) % 256
        total += subtotal

    return total


if __name__ == "__main__":
    p = Path(sys.argv[1])
    print(solve(p.read_text()))


def test():
    text = dedent(
        """
        HASH
        """
    ).strip()
    assert solve(text) == 52

    text = dedent(
        """
        rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
        """
    ).strip()
    assert solve(text) == 1320


def test_input():
    p = Path("15.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 506869
