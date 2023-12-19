import re
import sys
import pytest
from pathlib import Path
from textwrap import dedent


def solve(text: str) -> int:
    workflows_txt, parts_txt = text.split("\n\n", maxsplit=1)
    workflows = {}
    for workflow in workflows_txt.splitlines():
        name, conditions = workflow.split("{", maxsplit=1)  # }
        workflows[name] = conditions[:-1].split(",")

    parts = []
    pattern = re.compile(r"([a-z]+)=([0-9]+)")
    for part in parts_txt.splitlines():
        part_dict = {}
        for category, value in pattern.findall(part):
            part_dict[category] = int(value)
        parts.append(part_dict)

    total = 0
    for part in parts:
        current_workflow = "in"
        while current_workflow not in ["A", "R"]:
            for rule in workflows[current_workflow]:
                if "<" in rule:
                    category, value = rule.split("<")
                    value, workflow = value.split(":")
                    if part[category] < int(value):
                        current_workflow = workflow
                        break
                elif ">" in rule:
                    category, value = rule.split(">")
                    value, workflow = value.split(":")
                    if part[category] > int(value):
                        current_workflow = workflow
                        break
                else:
                    current_workflow = rule
                    break
        if current_workflow == "A":
            total += sum(part.values())
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
    assert solve(text) == 19114


def test_input():
    p = Path("19.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 476889
