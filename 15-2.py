import pytest
from pathlib import Path
from textwrap import dedent


def get_hash(word: str) -> int:
    total = 0
    for c in word:
        total = ((total + ord(c)) * 17) % 256
    return total


def solve(text: str) -> int:
    boxes = [{} for _ in range(256)]

    for word in text.strip().split(","):
        if "=" in word:
            label, focall = word.split("=")
            box_i = get_hash(label)
            boxes[box_i][label] = int(focall)
        else:
            label = word.split("-")[0]
            box_i = get_hash(label)
            boxes[box_i].pop(label, None)

    total = 0
    for box_i, box in enumerate(boxes):
        for label_i, (label, focall) in enumerate(box.items()):
            total += (box_i + 1) * (label_i + 1) * focall
    return total


if __name__ == "__main__":
    print(solve(input()))


def test():
    text = dedent(
        """
        rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
        """
    ).strip()
    assert solve(text) == 145


def test_input():
    p = Path("15.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 271384
