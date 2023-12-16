import sys
import pytest
from pathlib import Path
from textwrap import dedent


def solve(text: str) -> int:
    mappings = []
    lines = text.split("map:\n")
    seeds = list(
        map(int, lines[0].split("\n", maxsplit=1)[0].split(":", maxsplit=1)[1].split())
    )

    for split in lines[1:]:
        numbers = []
        for line in split.splitlines():
            if not line:
                break
            numbers.append(list(map(int, line.split())))

        if numbers:
            mappings.append(numbers)

    min_location: int | None = None
    for seed in seeds:
        value = seed
        for mapping in mappings:
            for dest_range, src_range, length in mapping:
                if src_range <= value <= src_range + length - 1:
                    value += dest_range - src_range
                    break
        if min_location is None or value < min_location:
            min_location = value

    assert min_location is not None
    return min_location


if __name__ == "__main__":
    p = Path(sys.argv[1])
    print(solve(p.read_text()))


def test():
    text = dedent(
        """
        seeds: 79 14 55 13

        seed-to-soil map:
        50 98 2
        52 50 48

        soil-to-fertilizer map:
        0 15 37
        37 52 2
        39 0 15

        fertilizer-to-water map:
        49 53 8
        0 11 42
        42 0 7
        57 7 4

        water-to-light map:
        88 18 7
        18 25 70

        light-to-temperature map:
        45 77 23
        81 45 19
        68 64 13

        temperature-to-humidity map:
        0 69 1
        1 0 69

        humidity-to-location map:
        60 56 37
        56 93 4
        """
    ).strip()
    assert solve(text) == 35


def test_input():
    p = Path("05.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 289863851
