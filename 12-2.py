from pathlib import Path
from textwrap import dedent


cache = {}


def get_valid_arrangements(
    acc: int,
    springs: str,
    spring_i: int,
    groups: list[int],
    group_i: int,
    spring: str | None = None,
) -> int:
    key = (acc, spring_i, group_i, spring)
    if key in cache:
        return cache[key]

    if spring_i >= len(springs):
        if acc:
            if group_i == len(groups) - 1 and acc == groups[group_i]:
                cache[key] = 1
                return 1
            cache[key] = 0
            return 0

        if group_i >= len(groups):
            cache[key] = 1
            return 1

        cache[key] = 0
        return 0

    spring = spring or springs[spring_i]
    if spring == ".":
        if acc:
            if group_i >= len(groups):
                cache[key] = 0
                return 0
            if acc != groups[group_i]:
                cache[key] = 0
                return 0
            r = get_valid_arrangements(
                acc=0,
                springs=springs,
                spring_i=spring_i + 1,
                groups=groups,
                group_i=group_i + 1,
            )
            cache[key] = r
            return r

        r = get_valid_arrangements(
            acc=0,
            springs=springs,
            spring_i=spring_i + 1,
            groups=groups,
            group_i=group_i,
        )
        cache[key] = r
        return r

    if spring == "#":
        if group_i >= len(groups):
            cache[key] = 0
            return 0
        r = get_valid_arrangements(
            acc=acc + 1,
            springs=springs,
            spring_i=spring_i + 1,
            groups=groups,
            group_i=group_i,
        )
        cache[key] = r
        return r

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
        r = a + b
        cache[key] = r
        return r

    return 0


def expand(springs: str, groups: list[int]) -> tuple[str, list[int]]:
    expanded_springs = []
    expanded_groups = []
    for _ in range(5):
        expanded_springs.append(springs)
        expanded_groups += groups

    return "?".join(expanded_springs), expanded_groups


def solve(text: str) -> int:
    springs_and_groups = [line.split() for line in text.splitlines()]
    total = 0
    for springs, groups in springs_and_groups:
        groups = [int(x) for x in groups.split(",")]
        springs, groups = expand(springs, groups)
        cache.clear()
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
    assert solve(text) == 525152

    p = Path("12.txt")
    if p.exists():
        text = p.read_text()
        assert solve(text) == 815364548481
