import pytest
from pathlib import Path
import itertools
from textwrap import dedent


def get_expanded_indexes(galaxies: list[list[str]]) -> tuple[list[int], list[int]]:
    vertical = []
    for i in range(len(galaxies)):
        for j in range(len(galaxies[i])):
            if galaxies[i][j] == "#":
                break
        else:
            vertical.append(i)

    horizontal = []
    for j in range(len(galaxies[0])):
        for i in range(len(galaxies)):
            if galaxies[i][j] == "#":
                break
        else:
            horizontal.append(j)

    return vertical, horizontal


def get_galaxies_index(galaxies: list[list[str]]) -> list[tuple[int, int]]:
    galaxies_index = []
    for i in range(len(galaxies)):
        for j in range(len(galaxies[i])):
            if galaxies[i][j] == "#":
                galaxies_index.append((i, j))
    return galaxies_index


def solve(text: str, expansion=2) -> int:
    galaxies = [[c for c in line] for line in text.splitlines()]
    vertical, horizontal = get_expanded_indexes(galaxies)

    galaxies_index = get_galaxies_index(galaxies)

    total = 0
    for a, b in itertools.combinations(galaxies_index, 2):
        # Cherk vertically
        vplus = 0
        for v in vertical:
            if a[0] < v < b[0] or b[0] < v < a[0]:
                vplus += 1

        # Check horizontally
        hplus = 0
        for h in horizontal:
            if a[1] < h < b[1] or b[1] < h < a[1]:
                hplus += 1

        subtotal = (
            abs(a[0] - b[0])
            + abs(a[1] - b[1])
            + (vplus * expansion)
            + (hplus * expansion)
            - hplus
            - vplus
        )
        total += subtotal

    return total


def main():
    text = Path("11.txt").read_text()
    print(solve(text))


if __name__ == "__main__":
    main()


def test():
    text = dedent(
        """
        ...#......
        .......#..
        #.........
        ..........
        ......#...
        .#........
        .........#
        ..........
        .......#..
        #...#.....
        """
    ).strip()
    assert solve(text, 100) == 8410


def test_input():
    p = Path("11.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text, 1000000) == 635832237682
