from copy import deepcopy
import sys
import pytest
from pathlib import Path
from textwrap import dedent


def traverse(
    workflow,
    workflows,
    ranges: dict[str, list[tuple[int, int]]],
    results: list[dict[str, list[tuple[int, int]]]],
):
    if workflow == "A":
        results.append(ranges)
        return
    if workflow == "R":
        return

    for rule in workflows[workflow]:
        if "<" in rule:
            category, value = rule.split("<")
            value, workflow = value.split(":")
            value = int(value)

            new_ranges_c = []
            new_current_ranges_c = []
            for a, b in ranges[category]:
                if b < value:
                    new_ranges_c.append((a, b))
                elif a < value:
                    new_ranges_c.append((a, value - 1))
                    new_current_ranges_c.append((value, b))
                else:
                    new_current_ranges_c.append((a, b))

            new_ranges = deepcopy(ranges)
            new_ranges[category] = new_ranges_c
            traverse(workflow, workflows, new_ranges, results)
            ranges[category] = new_current_ranges_c
        elif ">" in rule:
            category, value = rule.split(">")
            value, workflow = value.split(":")
            value = int(value)

            new_ranges_c = []
            new_current_ranges_c = []
            for a, b in ranges[category]:
                if a > value:
                    new_ranges_c.append((a, b))
                elif b > value:
                    new_ranges_c.append((value + 1, b))
                    new_current_ranges_c.append((a, value))
                else:
                    new_current_ranges_c.append((a, b))

            new_ranges = deepcopy(ranges)
            new_ranges[category] = new_ranges_c
            traverse(workflow, workflows, new_ranges, results)
            ranges[category] = new_current_ranges_c
        else:
            workflow = rule
            traverse(workflow, workflows, ranges, results)


def solve(text: str) -> int:
    workflows_txt, _ = text.split("\n\n", maxsplit=1)
    workflows = {}
    for workflow in workflows_txt.splitlines():
        name, conditions = workflow.split("{", maxsplit=1)  # }
        workflows[name] = conditions[:-1].split(",")

    results: list[dict[str, list[tuple[int, int]]]] = []
    ranges: dict[str, list[tuple[int, int]]] = {
        "x": [(1, 4000)],
        "m": [(1, 4000)],
        "a": [(1, 4000)],
        "s": [(1, 4000)],
    }
    traverse("in", workflows, ranges, results)

    total = 0
    for result in results:
        subtotal = 1
        for _, subranges in result.items():
            n = 0
            for a, b in subranges:
                n += b - a + 1
            subtotal *= n
        total += subtotal
    return total


if __name__ == "__main__":
    p = Path(sys.argv[1])
    print(solve(p.read_text()))


def test():
    text = dedent(
        """
        px{a<2006:qkq,m>2090:A,rfg}
        pv{a>1716:R,A}
        lnx{m>1548:A,A}
        rfg{s<537:gd,x>2440:R,A}
        qs{s>3448:A,lnx}
        qkq{x<1416:A,crn}
        crn{x>2662:A,R}
        in{s<1351:px,qqz}
        qqz{s>2770:qs,m<1801:hdj,R}
        gd{a>3333:R,R}
        hdj{m>838:A,pv}

        {x=787,m=2655,a=1222,s=2876}
        {x=1679,m=44,a=2067,s=496}
        {x=2036,m=264,a=79,s=2244}
        {x=2461,m=1339,a=466,s=291}
        {x=2127,m=1623,a=2188,s=1013}
        """
    ).strip()
    assert solve(text) == 167409079868000


def test_input():
    p = Path("19.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 132380153677887
