from pathlib import Path
from textwrap import dedent

START = "S"
VERTICAL_PIPE = "|"
HORIZONTAL_PIPE = "-"
NORTH_TO_EAST = "L"
NORTH_TO_WEST = "J"
SOUTH_TO_EAST = "F"
SOUTH_TO_WEST = "7"

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


def solve(text: str) -> int:
    maze = text.splitlines()
    i, j = get_start(maze)

    direction = None

    # Up
    if i > 0 and maze[i - 1][j] in [VERTICAL_PIPE, SOUTH_TO_EAST, SOUTH_TO_WEST]:
        i -= 1
        direction = UP
    # Down
    elif i < len(maze) - 1 and maze[i + 1][j] in [
        VERTICAL_PIPE,
        NORTH_TO_EAST,
        NORTH_TO_WEST,
    ]:
        i += 1
        direction = DOWN
    # Left
    elif j > 0 and maze[i][j - 1] in [HORIZONTAL_PIPE, SOUTH_TO_EAST, NORTH_TO_EAST]:
        j -= 1
        direction = LEFT
    # Right
    elif j < len(maze[i]) - 1 and maze[i][j + 1] in [
        HORIZONTAL_PIPE,
        SOUTH_TO_WEST,
        NORTH_TO_WEST,
    ]:
        j += 1
        direction = RIGHT

    steps = 1
    while maze[i][j] != START:
        pipe = maze[i][j]
        if pipe == VERTICAL_PIPE:
            if direction == UP:
                i -= 1
            else:
                i += 1
        elif pipe == SOUTH_TO_EAST:
            if direction == UP:
                j += 1
                direction = RIGHT
            else:
                i += 1
                direction = DOWN
        elif pipe == HORIZONTAL_PIPE:
            if direction == LEFT:
                j -= 1
            else:
                j += 1
        elif pipe == SOUTH_TO_WEST:
            if direction == UP:
                j -= 1
                direction = LEFT
            else:
                i += 1
                direction = DOWN
        elif pipe == NORTH_TO_WEST:
            if direction == DOWN:
                j -= 1
                direction = LEFT
            else:
                i -= 1
                direction = UP
        elif pipe == NORTH_TO_EAST:
            if direction == DOWN:
                j += 1
                direction = RIGHT
            else:
                i -= 1
                direction = UP

        steps += 1

    return steps // 2


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

    p = Path("10.txt")
    if p.exists():
        text = p.read_text()
        assert solve(text) == 6800
