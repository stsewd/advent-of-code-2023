from pathlib import Path
from textwrap import dedent


def get_valid_arrangements(acc: int, springs: str, valid_groups: list[int]) -> int:
    if not springs:
        if acc:
            if len(valid_groups) == 1 and acc == valid_groups[0]:
                return 1
            return 0

        if not valid_groups:
            return 1

        return 0

    spring = springs[0]
    if spring == ".":
        if acc:
            if not valid_groups:
                return 0
            if acc != valid_groups[0]:
                return 0
            return get_valid_arrangements(0, springs[1:], valid_groups[1:])
        return get_valid_arrangements(0, springs[1:], valid_groups)

    if spring == "#":
        if not valid_groups:
            return 0
        return get_valid_arrangements(acc + 1, springs[1:], valid_groups)

    if spring == "?":
        springs_a = "#" + springs[1:]
        springs_b = "." + springs[1:]
        a = get_valid_arrangements(acc, springs_a, valid_groups)
        b = get_valid_arrangements(acc, springs_b, valid_groups)
        return a + b

    return 0


def solve(text: str) -> int:
    springs_and_groups = [line.split() for line in text.splitlines()]
    total = 0
    for springs, groups in springs_and_groups:
        total += get_valid_arrangements(0, springs, [int(x) for x in groups.split(",")])
    return total


def main():
    text = Path("12.txt").read_text()
    print(solve(text))


if __name__ == "__main__":
    main()


def test():
    text = dedent(
        """
        ???.### 1,1,3
        .??..??...?##. 1,1,3
        ?#?#?#?#?#?#?#? 1,3,1,6
        ????.#...#... 4,1,1
        ????.######..#####. 1,6,5
        ?###???????? 3,2,1
        """
    ).strip()
    assert solve(text) == 21
