from pathlib import Path
import itertools
from textwrap import dedent


def expand(galaxies: list[list[str]]):
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

    # Expand vertically
    for e, i in enumerate(vertical):
        galaxies.insert(i + e, ["."] * len(galaxies[0]))

    # Expand horizontally
    for e, j in enumerate(horizontal):
        for i in range(len(galaxies)):
            galaxies[i].insert(j + e, ".")


def get_galaxies_index(galaxies: list[list[str]]) -> list[tuple[int, int]]:
    galaxies_index = []
    z = 1
    for i in range(len(galaxies)):
        for j in range(len(galaxies[i])):
            if galaxies[i][j] == "#":
                galaxies_index.append((i, j, z))
                z += 1
    return galaxies_index


def solve(text: str) -> int:
    galaxies = [[c for c in line] for line in text.splitlines()]
    expand(galaxies)

    galaxies_index = get_galaxies_index(galaxies)

    total = 0
    for a, b in itertools.combinations(galaxies_index, 2):
        subtotal = abs(a[0] - b[0]) + abs(a[1] - b[1])
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
    assert solve(text) == 374

    text = Path("11.txt").read_text()
    assert solve(text) == 9509330
