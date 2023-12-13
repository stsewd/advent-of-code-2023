import pytest
from pathlib import Path
from textwrap import dedent


def get_valid_arrangements(
    acc: int,
    springs: str,
    spring_i: int,
    groups: list[int],
    group_i: int,
    spring: str | None = None,
) -> int:
    if spring_i >= len(springs):
        if acc:
            if group_i == len(groups) - 1 and acc == groups[group_i]:
                return 1
            return 0

        if group_i >= len(groups):
            return 1

        return 0

    spring = spring or springs[spring_i]
    if spring == ".":
        if acc:
            if group_i >= len(groups):
                return 0
            if acc != groups[group_i]:
                return 0
            return get_valid_arrangements(
                acc=0,
                springs=springs,
                spring_i=spring_i + 1,
                groups=groups,
                group_i=group_i + 1,
            )

        return get_valid_arrangements(
            acc=0,
            springs=springs,
            spring_i=spring_i + 1,
            groups=groups,
            group_i=group_i,
        )

    if spring == "#":
        if group_i >= len(groups):
            return 0
        return get_valid_arrangements(
            acc=acc + 1,
            springs=springs,
            spring_i=spring_i + 1,
            groups=groups,
            group_i=group_i,
        )

    if spring == "?":
        a = get_valid_arrangements(
            acc=acc,
            springs=springs,
            spring_i=spring_i,
            groups=groups,
            group_i=group_i,
            spring="#",
        )
        b = get_valid_arrangements(
            acc=acc,
            springs=springs,
            spring_i=spring_i,
            groups=groups,
            group_i=group_i,
            spring=".",
        )
        return a + b

    return 0


def solve(text: str) -> int:
    springs_and_groups = [line.split() for line in text.splitlines()]
    total = 0
    for springs, groups in springs_and_groups:
        groups = [int(x) for x in groups.split(",")]
        total += get_valid_arrangements(
            acc=0,
            springs=springs,
            spring_i=0,
            groups=groups,
            group_i=0,
        )
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


def test_input():
    p = Path("12.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 6488
