from pathlib import Path
from textwrap import dedent


def solve(text: str) -> int:
    lines = text.splitlines()
    times = list(map(int, lines[0].split(":", maxsplit=1)[1].split()))
    distances = list(map(int, lines[1].split(":", maxsplit=1)[1].split()))

    total = 1
    for i in range(len(times)):
        t = times[i]
        d = distances[i]
        half = t // 2
        for i in range(1, half + 1):
            r = i * (t - i)
            if r > d:
                subtotal = ((half - i) + 1) * 2
                if t % 2 == 0:
                    subtotal -= 1
                total *= subtotal
                break
    return total


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
    assert solve(text) == 288

    text = Path("06.txt").read_text()
    assert solve(text) == 3317888
