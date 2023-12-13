from pathlib import Path
from textwrap import dedent


def solve(text: str) -> int:
    total = 0
    for line in text.splitlines():
        winning_numbers, numbers = line.split(":", maxsplit=1)[1].split("|", maxsplit=1)
        winning_numbers = set(winning_numbers.split())
        numbers = set(numbers.split())
        resulted_numbers = winning_numbers.intersection(numbers)
        if resulted_numbers:
            total += 2 ** (len(resulted_numbers) - 1)
    return total


def main():
    text = Path("04.txt").read_text()
    print(solve(text))


if __name__ == "__main__":
    main()


def test():
    text = dedent(
        """
        Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
        Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
        Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
        Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
        Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
        """
    ).strip()
    assert solve(text) == 13

    p = Path("03.txt")
    if p.exists():
        text = p.read_text()
        assert solve(text) == 26914
