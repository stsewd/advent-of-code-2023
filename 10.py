from pathlib import Path
from textwrap import dedent
import sys
print(sys.getrecursionlimit())
sys.setrecursionlimit(100000)


START = "S"
VERTICAL_PIPE = "|"
HORIZONTAL_PIPE = "-"
NORTH_TO_EAST = "L"
NORTH_TO_WEST = "J"
SOUTH_TO_EAST = "F"
SOUTH_TO_WEST = "7"
PIPES = [
    VERTICAL_PIPE,
    HORIZONTAL_PIPE,
    NORTH_TO_EAST,
    NORTH_TO_WEST,
    SOUTH_TO_EAST,
    SOUTH_TO_WEST,
]

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

def get_start(maze: list[str]) -> tuple[int, int]:
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == START:
                return (i, j)
    return (0, 0)


def solve_maze(maze: list[str], start: tuple[int, int], previous=None) -> int:
    i, j = start
    current_pipe = maze[i][j]

    # Check up
    if previous != UP and current_pipe in [START, VERTICAL_PIPE, NORTH_TO_EAST, NORTH_TO_WEST] and i > 0:
        pipe = maze[i - 1][j]
        if pipe == START:
            return 1
        if pipe in [VERTICAL_PIPE, SOUTH_TO_EAST, SOUTH_TO_WEST]:
            r = solve_maze(maze, (i - 1, j), DOWN)
            if r != -1:
                return r + 1
    # Check down
    if previous != DOWN and current_pipe in [START, VERTICAL_PIPE, SOUTH_TO_EAST, SOUTH_TO_WEST] and i < len(maze) - 1:
        pipe = maze[i + 1][j]
        if pipe == START:
            return 1
        if pipe in [VERTICAL_PIPE, NORTH_TO_EAST, NORTH_TO_WEST]:
            r = solve_maze(maze, (i + 1, j), UP)
            if r != -1:
                return r + 1

    # Check left
    if previous != LEFT and current_pipe in [START, HORIZONTAL_PIPE, NORTH_TO_WEST, SOUTH_TO_WEST] and j > 0:
        pipe = maze[i][j - 1]
        if pipe == START:
            return 1
        if pipe in [HORIZONTAL_PIPE, SOUTH_TO_EAST, NORTH_TO_EAST]:
            r = solve_maze(maze, (i, j - 1), RIGHT)
            if r != -1:
                return r + 1

    # Check right
    if previous != RIGHT and current_pipe in [START, HORIZONTAL_PIPE, NORTH_TO_EAST, SOUTH_TO_EAST] and j < len(maze[i]) - 1:
        pipe = maze[i][j + 1]
        if pipe == START:
            return 1
        if pipe in [HORIZONTAL_PIPE, SOUTH_TO_WEST, NORTH_TO_WEST]:
            r = solve_maze(maze, (i, j + 1), LEFT)
            if r != -1:
                return r + 1

    return -1


def solve(text: str) -> int:
    maze = text.splitlines()
    return solve_maze(maze, get_start(maze), None) // 2


def main():
    text = Path("10.txt").read_text()
    print(solve(text))


if __name__ == "__main__":
    main()


def test():
    text = dedent(
        """
        -L|F7
        7S-7|
        L|7||
        -L-J|
        L|-JF
        """
    ).strip()
    assert solve(text) == 4

    text = dedent(
        """
        7-F7-
        .FJ|7
        SJLL7
        |F--J
        LJ.LJ
        """
    ).strip()
    assert solve(text) == 8

    text = Path("10.txt").read_text()
    assert solve(text) == 6800
