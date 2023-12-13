import pytest
from functools import reduce
from pathlib import Path
from textwrap import dedent
from operator import mul


def get_power(game_data: str) -> int:
    min_cubes_number = {}
    for game_set in game_data.split(";"):
        cubes_data = game_set.strip().split(",")
        for cube_data in cubes_data:
            n, color = cube_data.strip().split(maxsplit=1)
            n = int(n)
            min_cubes_number.setdefault(color, n)
            if n > min_cubes_number[color]:
                min_cubes_number[color] = n
    return reduce(mul, min_cubes_number.values())


def solve(text: str) -> int:
    total = 0
    for line in text.splitlines():
        _, game_data = line.split(":", maxsplit=1)
        power = get_power(game_data.strip())
        total += power
    return total


def main():
    input_text = Path("02.txt").read_text()
    print(solve(input_text))


if __name__ == "__main__":
    main()


def test():
    text = dedent(
        """
        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
        """
    ).strip()
    assert solve(text) == 2286


def test_input():
    p = Path("02.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 72513
