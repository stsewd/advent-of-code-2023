import sys
import pytest
from pathlib import Path
from textwrap import dedent


def solve(text: str) -> int:
    coordinates = {}
    for i, line in enumerate(text.splitlines()):
        point_a, point_b = line.split("~")
        point_a = list(map(int, point_a.split(",")))
        point_b = list(map(int, point_b.split(",")))
        coordinates[i] = (point_a, point_b)

    # Sort by the z coordinate of the first point.
    to_process = sorted(coordinates.keys(), key=lambda k: coordinates[k][0][2])
    while to_process:
        current = to_process.pop(0)
        current_a, current_b = coordinates[current]

        new_z = 0
        coordinates_below = [
            k for k, (_, bb) in coordinates.items() if bb[2] < current_a[2]
        ]
        # Sort by the z coordinate of the second point.
        coordinates_below.sort(key=lambda k: coordinates[k][1][2], reverse=True)
        while coordinates_below:
            below = coordinates_below.pop(0)
            below_a, below_b = coordinates[below]
            x_intersects = (
                below_a[0] <= current_a[0] <= below_b[0]
                or below_a[0] <= current_b[0] <= below_b[0]
                or current_a[0] <= below_a[0] <= current_b[0]
                or current_a[0] <= below_b[0] <= current_b[0]
            )
            y_intersects = (
                below_a[1] <= current_a[1] <= below_b[1]
                or below_a[1] <= current_b[1] <= below_b[1]
                or current_a[1] <= below_a[1] <= current_b[1]
                or current_a[1] <= below_b[1] <= current_b[1]
            )
            if x_intersects and y_intersects:
                new_z = below_b[2] + 1
                break

        diff = current_a[2] - new_z
        coordinates[current] = (
            (current_a[0], current_a[1], current_a[2] - diff),
            (current_b[0], current_b[1], current_b[2] - diff),
        )

    hold = {}

    # Sort by the z coordinate of the first point.
    for current_block in coordinates:
        current_a, current_b = coordinates[current_block]
        hold.setdefault(current_b[2], {}).setdefault(current_block, set())
        for above, (above_a, above_b) in coordinates.items():
            z = current_b[2] + 1
            if above_a[2] == z:
                x_intersects = (
                    above_a[0] <= current_a[0] <= above_b[0]
                    or above_a[0] <= current_b[0] <= above_b[0]
                    or current_a[0] <= above_a[0] <= current_b[0]
                    or current_a[0] <= above_b[0] <= current_b[0]
                )
                y_intersects = (
                    above_a[1] <= current_a[1] <= above_b[1]
                    or above_a[1] <= current_b[1] <= above_b[1]
                    or current_a[1] <= above_a[1] <= current_b[1]
                    or current_a[1] <= above_b[1] <= current_b[1]
                )
                if x_intersects and y_intersects:
                    hold[current_b[2]][current_block].add(above)

    count = 0
    for blocks in hold.values():
        for block, block_set in blocks.items():
            current_set = block_set.copy()
            for block_b, block_set_b in blocks.items():
                if block_b == block:
                    continue
                current_set -= block_set_b

            if not current_set:
                count += 1
    return count


if __name__ == "__main__":
    p = Path(sys.argv[1])
    print(solve(p.read_text()))


def test():
    text = dedent(
        """
        1,0,1~1,2,1
        0,0,2~2,0,2
        0,2,3~2,2,3
        0,0,4~0,2,4
        2,0,5~2,2,5
        0,1,6~2,1,6
        1,1,8~1,1,9
        """
    ).strip()
    assert solve(text) == 5


def test_input():
    p = Path("22.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 441
