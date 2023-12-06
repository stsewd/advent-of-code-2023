from pathlib import Path
from textwrap import dedent


def solve(text: str) -> int:
    lines = text.splitlines()
    time = int("".join(lines[0].split(":", maxsplit=1)[1].split()))
    distance = int("".join(lines[1].split(":", maxsplit=1)[1].split()))

    half = time // 2
    for i in range(1, half + 1):
        r = i * (time - i)
        if r > distance:
            subtotal = ((half - i) + 1) * 2
            if time % 2 == 0:
                subtotal -= 1
            return subtotal
    return 0


def main():
    text = Path("06.txt").read_text()
    print(solve(text))


if __name__ == "__main__":
    main()


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

    text = Path("06.txt").read_text()
    assert solve(text) == 0
