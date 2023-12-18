import re
import sys
import pytest
from pathlib import Path
from textwrap import dedent


UP = "U"
DOWN = "D"
RIGHT = "R"
LEFT = "L"

N_TO_DIRECTION = {
    0: RIGHT,
    1: DOWN,
    2: LEFT,
    3: UP,
}


def area(points: list[tuple[int, int]]) -> float:
    """
    Get the area of a polygon using the shoelace formula.

    See https://en.wikipedia.org/wiki/Shoelace_formula.
    """
    overlaped_points = zip(points, points[1:] + [points[0]])
    return abs(sum(x0 * y1 - x1 * y0 for ((x0, y0), (x1, y1)) in overlaped_points)) / 2


def solve(text: str) -> int:
    lines = text.splitlines()
    intersections: list[tuple[int, int]] = [(0, 0)]

    pattern = re.compile(r".+\(#([a-z0-9]+)\)")
    steps = 0
    for line in lines:
        point = intersections[-1]
        hex_color = pattern.match(line).group(1)
        direction = N_TO_DIRECTION[int(hex_color[-1])]
        n = int(hex_color[:-1], 16)
        steps += n
        if direction == UP:
            intersections.append((point[0] - n, point[1]))
        elif direction == DOWN:
            intersections.append((point[0] + n, point[1]))
        elif direction == RIGHT:
            intersections.append((point[0], point[1] + n))
        elif direction == LEFT:
            intersections.append((point[0], point[1] - n))

    intersections.pop(-1)
    # Use Pick's theorem to calculate inner points of the polygon,
    # and add the number of steps to get the total number of points.
    # See https://en.wikipedia.org/wiki/Pick's_theorem.
    interior_points = area(intersections) - steps / 2 + 1
    return int(interior_points + steps)


if __name__ == "__main__":
    p = Path(sys.argv[1])
    print(solve(p.read_text()))


def test():
    text = dedent(
        """
        R 6 (#70c710)
        D 5 (#0dc571)
        L 2 (#5713f0)
        D 2 (#d2c081)
        R 2 (#59c680)
        D 2 (#411b91)
        L 5 (#8ceee2)
        U 2 (#caa173)
        L 1 (#1b58a2)
        U 2 (#caa171)
        R 2 (#7807d2)
        U 3 (#a77fa3)
        L 2 (#015232)
        U 2 (#7a21e3)
        """
    ).strip()
    assert solve(text) == 952408144115


def test_input():
    p = Path("18.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 177243763226648
