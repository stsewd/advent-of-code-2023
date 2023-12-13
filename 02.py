from pathlib import Path
from textwrap import dedent


def is_possible(game_data: str, setup: dict[str, int]) -> bool:
    total_cubes_allowed = sum(setup.values())
    for game_set in game_data.split(";"):
        cubes_data = game_set.strip().split(",")
        total_cubes = 0
        for cube_data in cubes_data:
            n, color = cube_data.strip().split(maxsplit=1)
            n = int(n)
            if n > setup[color]:
                return False
            total_cubes += n
            if total_cubes > total_cubes_allowed:
                return False
    return True


def solve(text: str, setup: dict[str, int]) -> int:
    total = 0
    for i, line in enumerate(text.splitlines(), start=1):
        _, game_data = line.split(":", maxsplit=1)
        if is_possible(game_data.strip(), setup):
            total += i
    return total


def main():
    input_text = Path("02.txt").read_text()
    print(solve(input_text, setup={"red": 12, "green": 13, "blue": 14}))


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
    assert solve(text, setup={"red": 12, "green": 13, "blue": 14}) == 8

    p = Path("02.txt")
    if p.exists():
        text = p.read_text()
        assert solve(text, setup={"red": 12, "green": 13, "blue": 14}) == 2162
