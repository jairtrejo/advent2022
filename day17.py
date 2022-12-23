import fileinput
from itertools import cycle, groupby

PIECES = """
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""

pieces = cycle(
    list(g)
    for k, g in groupby(PIECES.strip().split("\n"), key=lambda l: l != "")
    if k
)


def collides(piece, x, y, floor):
    pass


def push(piece, x, direction):
    if direction == "<":
        return x - 1 if x > 0 else x
    if direction == ">":
        return x + 1 if (x + len(piece[0])) < 6 else x


with fileinput.input() as f:
    jets = cycle(f.readline().strip())
    world = [[0] * 7]

    for piece in pieces:
        x, y = 2, max(floor) + 3
        for jet in jets:
            new_x = push(piece, x, jet)
            if new_x != x and not collides(piece, new_x, y, world)
