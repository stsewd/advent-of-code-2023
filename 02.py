import sys
import pytest
from pathlib import Path
from textwrap import dedent


def is_possible(game_data: str, setup: dict[str, int]) -> bool:
    for game_set in game_data.split(";"):
        cubes_data = game_set.strip().split(",")
        for cube_data in cubes_data:
            n, color = cube_data.strip().split(maxsplit=1)
            n = int(n)
            if n > setup[color]:
                return False
    return True


def solve(text: str, setup: dict[str, int]) -> int:
    total = 0
    for i, line in enumerate(text.splitlines(), start=1):
        _, game_data = line.split(":", maxsplit=1)
        if is_possible(game_data.strip(), setup):
            total += i
    return total


if __name__ == "__main__":
    p = Path(sys.argv[1])
    print(solve(p.read_text(), setup={"red": 12, "green": 13, "blue": 14}))


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
    assert solve(text, setup={"red": 12, "green": 13, "blue": 14}) == 8


def test_input():
    p = Path("02.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text, setup={"red": 12, "green": 13, "blue": 14}) == 2162
