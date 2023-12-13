from pathlib import Path
from textwrap import dedent


def get_pascal_triangle_row(row):
    current_row = [1]
    for i in range(1, row + 1):
        new_row = [1]
        for j in range(i - 1):
            a = current_row[j]
            b = current_row[j + 1]
            new_row.append(a + b)
        new_row.append(1)
        current_row = new_row
    return current_row


def solve(text: str) -> int:
    """
    The solutions follow a pattern found in the Pascal triangle,
    with each number alternating between adding and subtracting.
    This solves the problem in linear time.
    """
    lines = text.splitlines()
    lines = [list(map(int, line.split())) for line in lines]

    n = len(lines[0])
    values = get_pascal_triangle_row(n)

    total = 0
    for line in lines:
        add = len(line) % 2 != 0
        for a, b in zip(line, values):
            r = a * b
            if add:
                total += r
            else:
                total -= r
            add = not add
    return total


def main():
    text = Path("09.txt").read_text()
    print(solve(text))


if __name__ == "__main__":
    main()


def test():
    text = dedent(
        """
        0 3 6 9 12 15
        1 3 6 10 15 21
        10 13 16 21 30 45
        """
    ).strip()
    assert solve(text) == 114

    p = Path("09.txt")
    if p.exists():
        text = p.read_text()
        assert solve(text) == 1974913025
