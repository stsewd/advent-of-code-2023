import pytest
from pathlib import Path
from textwrap import dedent


def get_ranges(
    istart: int, ilength: int, mappings: list[tuple[int, int, int]]
) -> list[tuple[int, int]]:
    ranges = []
    iend = istart + ilength - 1
    for dest_start, src_start, length in mappings:
        src_end = src_start + length - 1
        if istart < src_start:
            if iend < src_start:
                ranges.append((istart, iend - istart + 1))
                return ranges

            ranges.append((istart, src_start - istart))
            istart = src_start

        if src_start <= istart <= src_end:
            if iend <= src_end:
                new_istart = istart + (dest_start - src_start)
                ranges.append((new_istart, iend - istart + 1))
                return ranges

            new_istart = istart + (dest_start - src_start)
            ranges.append((new_istart, src_end - istart + 1))
            istart = src_end + 1

    ranges.append((istart, iend - istart + 1))
    return ranges


def solve(text: str) -> int:
    mappings = []
    lines = text.split("map:\n")
    all_seeds = list(
        map(int, lines[0].split("\n", maxsplit=1)[0].split(":", maxsplit=1)[1].split())
    )
    seeds = [(all_seeds[i], all_seeds[i + 1]) for i in range(0, len(all_seeds), 2)]

    for split in lines[1:]:
        numbers = []
        for line in split.splitlines():
            if not line:
                break
            numbers.append(list(map(int, line.split())))

        if numbers:
            numbers.sort(key=lambda x: x[1])
            mappings.append(numbers)

    for mapping in mappings:
        new_seeds = []
        for seed_start, seed_length in seeds:
            ranges = get_ranges(seed_start, seed_length, mapping)
            new_seeds.extend(ranges)
        seeds = new_seeds

    return min(start for start, _ in seeds)


def main():
    text = Path("05.txt").read_text()
    print(solve(text))


if __name__ == "__main__":
    main()


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
    assert solve(text) == 46


def test_input():
    p = Path("05.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 60568880
