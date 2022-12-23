import fileinput
import math
from itertools import pairwise


def draw_sand(lines, sand):
    left = min(min(x0, x1) for x0, _, x1, _ in lines if x0 != -math.inf)
    # top = min(min(y0, y1) for _, y0, _, y1 in lines)
    right = max(max(x0, x1) for x0, _, x1, _ in lines if x0 != -math.inf)
    bottom = max(max(y0, y1) for _, y0, _, y1 in lines)

    sand_left = min(x for x, y in sand)
    sand_right = max(x for x, y in sand)

    left = min(left, sand_left)
    right = max(right, sand_right)

    for row in range(0, bottom + 1):
        for col in range(left, right + 1):
            if (col, row) == (500, 0):
                print("+", end="")
            elif (col, row) in sand:
                print(".", end="")
            elif blocked((col, row), lines, sand):
                print("#", end="")
            else:
                print(" ", end="")
        print()


def blocked(position, lines=[], sand=set()):
    x, y = position

    if position in sand:
        return True

    for x0, y0, x1, y1 in lines:
        if x0 == x1:
            result = x == x0 and ((y0 <= y <= y1) or (y1 <= y <= y0))
        else:
            result = y == y0 and ((x0 <= x <= x1) or (x1 <= x <= x0))

        if result:
            return True

    return False


def move_sand(start, lines=[], sand=set()):
    x, y = start
    if not blocked((x, y + 1), lines, sand):
        return (x, y + 1)
    elif not blocked((x - 1, y + 1), lines, sand):
        return (x - 1, y + 1)
    elif not blocked((x + 1, y + 1), lines, sand):
        return (x + 1, y + 1)
    else:
        return start


def simulate(lines, void):
    sand = set()
    units = 0
    start = (_, start_y) = (500, 0)
    while start_y < void:
        end = move_sand(start, lines, sand)
        if end == (500, 0):
            units += 1
            break
        elif end == start:
            if end in sand:
                print("Error")
            sand.add(end)
            start = (_, start_y) = (500, 0)
            units += 1
        else:
            start = (_, start_y) = end

    return units


with fileinput.input() as f:
    lines = []

    for l in f:
        lines += [
            (x0, y0, x1, y1)
            for ((x0, y0), (x1, y1)) in pairwise(
                tuple(map(int, p.strip().split(","))) for p in l.split(" -> ")
            )
        ]

    void = max(max(y1, y0) for (_, y0, _, y1) in lines)

    units = simulate(lines, void)
    print(units)

    units = simulate(
        [*lines, (-math.inf, void + 2, math.inf, void + 2)], void + 2
    )
    print(units)
