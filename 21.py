import sys
import pytest
from pathlib import Path
from textwrap import dedent

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"


def is_in_range(matrix, i, j):
    return i >= 0 and j >= 0 and i < len(matrix) and j < len(matrix[i])


def get_start(matrix) -> tuple[int, int]:
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == "S":
                return i, j
    return 0, 0


cache = {}


def traverse(matrix, start, steps, direction):
    i, j = start

    if not is_in_range(matrix, i, j):
        return

    if matrix[i][j] == "#":
        return

    if steps == 0:
        matrix[i][j] = "X"
        cache[i, j, direction, True] = steps
        return
    if steps < 0:
        return

    key = (i, j, direction, steps)
    if key in cache:
        return

    if direction == RIGHT:
        while is_in_range(matrix, i, j) and matrix[i][j] != "#" and steps >= 0:
            if steps % 2 == 0 or steps == 0:
                matrix[i][j] = "X"

            cache[i, j, direction, steps] = True

            if is_in_range(matrix, i - 1, j):
                traverse(matrix, (i - 1, j), steps - 1, UP)
            if is_in_range(matrix, i + 1, j):
                traverse(matrix, (i + 1, j), steps - 1, DOWN)
            j += 1
            steps -= 1
    elif direction == LEFT:
        while is_in_range(matrix, i, j) and matrix[i][j] != "#" and steps >= 0:
            if steps % 2 == 0 or steps == 0:
                matrix[i][j] = "X"

            cache[i, j, direction, steps] = True

            if is_in_range(matrix, i - 1, j):
                traverse(matrix, (i - 1, j), steps - 1, UP)
            if is_in_range(matrix, i + 1, j):
                traverse(matrix, (i + 1, j), steps - 1, DOWN)
            j -= 1
            steps -= 1
    elif direction == UP:
        while is_in_range(matrix, i, j) and matrix[i][j] != "#" and steps >= 0:
            if steps % 2 == 0 or steps == 0:
                matrix[i][j] = "X"

            cache[i, j, direction, steps] = True

            if is_in_range(matrix, i, j - 1):
                traverse(matrix, (i, j - 1), steps - 1, LEFT)
            if is_in_range(matrix, i, j + 1):
                traverse(matrix, (i, j + 1), steps - 1, RIGHT)
            i -= 1
            steps -= 1
    elif direction == DOWN:
        while is_in_range(matrix, i, j) and matrix[i][j] != "#" and steps >= 0:
            if steps % 2 == 0 or steps == 0:
                matrix[i][j] = "X"

            cache[i, j, direction, steps] = True

            if is_in_range(matrix, i, j - 1):
                traverse(matrix, (i, j - 1), steps - 1, LEFT)
            if is_in_range(matrix, i, j + 1):
                traverse(matrix, (i, j + 1), steps - 1, RIGHT)
            i += 1
            steps -= 1
    return


def solve(text: str, steps) -> int:
    matrix = [list(line) for line in text.splitlines()]
    start = get_start(matrix)
    cache.clear()
    traverse(matrix, start, steps, RIGHT)
    traverse(matrix, start, steps, LEFT)

    total = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == "X":
                total += 1
    return total


if __name__ == "__main__":
    p = Path(sys.argv[1])
    print(solve(p.read_text(), 64))


def test():
    text = dedent(
        """
        ...........
        .....###.#.
        .###.##..#.
        ..#.#...#..
        ....#.#....
        .##..S####.
        .##..#...#.
        .......##..
        .##.#.####.
        .##..##.##.
        ...........
        """
    ).strip()
    assert solve(text, 6) == 16


def test_input():
    p = Path("21.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text, 64) == 3830
