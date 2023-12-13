from pathlib import Path
from textwrap import dedent


def find_middle(pattern: list[int], no_valid: int) -> int:
    for i in range(len(pattern) - 1):
        index = len(pattern) - i - 1
        start = index
        if start == no_valid:
            continue
        end = min((len(pattern) - index), index)
        for j in range(index, index + end):
            index -= 1
            if pattern[j] != pattern[index]:
                break
        else:
            return start
    return -1


def get_result(pattern: list[str]) -> int:
    vertical = []
    for j in range(len(pattern[0])):
        n = 0
        for i in range(len(pattern)):
            if pattern[i][j] == "#":
                n += 2**i
        vertical.append(n)

    original_index = find_middle(vertical, -1)
    for i in range(len(vertical)):
        original = vertical[i]
        for j in range(len(pattern)):
            # Flip bit
            vertical[i] = original ^ 2**j
            index = find_middle(vertical, original_index)
            if index != -1:
                return index
        vertical[i] = original

    horizontal = []
    for i in range(len(pattern)):
        n = 0
        for j in range(len(pattern[0])):
            if pattern[i][j] == "#":
                n += 2**j
        horizontal.append(n)

    original_index = find_middle(horizontal, -1)
    for i in range(len(horizontal)):
        original = horizontal[i]
        for j in range(len(pattern[0])):
            # Flip bit
            horizontal[i] = original ^ 2**j
            index = find_middle(horizontal, original_index)
            if index != -1:
                return index * 100
        horizontal[i] = original

    return 0


def solve(text: str) -> int:
    total = 0
    for patter in text.split("\n\n"):
        total += get_result(patter.splitlines())

    return total


def main():
    text = Path("13.txt").read_text()
    print(solve(text))


if __name__ == "__main__":
    main()


def test():
    text = dedent(
        """
        #.##..##.
        ..#.##.#.
        ##......#
        ##......#
        ..#.##.#.
        ..##..##.
        #.#.##.#.

        #...##..#
        #....#..#
        ..##..###
        #####.##.
        #####.##.
        ..##..###
        #....#..#
        """
    ).strip()
    assert solve(text) == 400

    p = Path("13.txt")
    if p.exists():
        text = p.read_text()
        assert solve(text) == 33438
