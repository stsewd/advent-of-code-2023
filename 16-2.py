import sys
import pytest
from pathlib import Path
from textwrap import dedent

UP = "^"
DOWN = "v"
LEFT = "<"
RIGHT = ">"


def traverse(
    matrix: list[list[str]],
    start: tuple[int, int],
    direction: str,
    beans: set[tuple[int, int, str]],
):
    i, j = start
    if i < 0 or i >= len(matrix) or j < 0 or j >= len(matrix[i]):
        return

    if (i, j, direction) in beans:
        return
    beans.add((i, j, direction))

    if matrix[i][j] == "|":
        if direction in (LEFT, RIGHT):
            traverse(matrix, (i - 1, j), UP, beans)
            traverse(matrix, (i + 1, j), DOWN, beans)
        if direction == UP:
            traverse(matrix, (i - 1, j), UP, beans)
        elif direction == DOWN:
            traverse(matrix, (i + 1, j), DOWN, beans)
        return

    if matrix[i][j] == "-":
        if direction in (UP, DOWN):
            traverse(matrix, (i, j - 1), LEFT, beans)
            traverse(matrix, (i, j + 1), RIGHT, beans)
        if direction == LEFT:
            traverse(matrix, (i, j - 1), LEFT, beans)
        elif direction == RIGHT:
            traverse(matrix, (i, j + 1), RIGHT, beans)
        return

    if matrix[i][j] == "\\":
        if direction == UP:
            traverse(matrix, (i, j - 1), LEFT, beans)
        elif direction == DOWN:
            traverse(matrix, (i, j + 1), RIGHT, beans)
        elif direction == LEFT:
            traverse(matrix, (i - 1, j), UP, beans)
        elif direction == RIGHT:
            traverse(matrix, (i + 1, j), DOWN, beans)
        return

    if matrix[i][j] == "/":
        if direction == UP:
            traverse(matrix, (i, j + 1), RIGHT, beans)
        elif direction == DOWN:
            traverse(matrix, (i, j - 1), LEFT, beans)
        elif direction == LEFT:
            traverse(matrix, (i + 1, j), DOWN, beans)
        elif direction == RIGHT:
            traverse(matrix, (i - 1, j), UP, beans)
        return

    while (
        i >= 0
        and i < len(matrix)
        and j >= 0
        and j < len(matrix[i])
        and matrix[i][j] == "."
    ):
        beans.add((i, j, direction))
        if direction == RIGHT:
            j += 1
        elif direction == LEFT:
            j -= 1
        elif direction == UP:
            i -= 1
        elif direction == DOWN:
            i += 1

    traverse(matrix, (i, j), direction, beans)


def solve(text: str) -> int:
    matrix = [[c for c in line] for line in text.splitlines()]
    total = 0
    for i in range(len(matrix)):
        beans = set()
        traverse(matrix, (i, 0), RIGHT, beans)
        n_beans = len(set((i, j) for i, j, _ in beans))
        total = max(total, n_beans)

    for j in range(len(matrix[0])):
        beans = set()
        traverse(matrix, (0, j), DOWN, beans)
        n_beans = len(set((i, j) for i, j, _ in beans))
        total = max(total, n_beans)

    for i in range(len(matrix)):
        beans = set()
        traverse(matrix, (i, len(matrix[i]) - 1), LEFT, beans)
        n_beans = len(set((i, j) for i, j, _ in beans))
        total = max(total, n_beans)

    for j in range(len(matrix[0])):
        beans = set()
        traverse(matrix, (len(matrix) - 1, j), UP, beans)
        n_beans = len(set((i, j) for i, j, _ in beans))
        total = max(total, n_beans)

    return total


if __name__ == "__main__":
    p = Path(sys.argv[1])
    print(solve(p.read_text()))


def test():
    text = dedent(
        r"""
        .|...\....
        |.-.\.....
        .....|-...
        ........|.
        ..........
        .........\
        ..../.\\..
        .-.-/..|..
        .|....-|.\
        ..//.|....
        """
    ).strip()
    assert solve(text) == 51


def test_input():
    p = Path("16.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 7313
