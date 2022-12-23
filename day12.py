import fileinput
import math
from collections import defaultdict
from itertools import chain, pairwise


def can_jump(o, d):
    if o is None or d is None:
        return False

    if o == "E":
        o = "z"
    if d == "E":
        d = "z"
    if o == "S":
        o = "a"
    if d == "S":
        d = "a"

    return (ord(d) - ord(o)) <= 1


neighbors = defaultdict(list)
reverse_neighbors = defaultdict(list)


def find_path(neighbors, origin, destination):
    unvisited = {node for node in neighbors.keys() if node != origin}
    unvisited.add(origin)

    distances = {node: math.inf for node in neighbors.keys() if node != origin}
    distances[origin] = 0

    from_ = {node: None for node in neighbors.keys()}

    current = origin
    while True:
        candidates = [n for n in neighbors[current] if n in unvisited]
        for c in candidates:
            if distances[c] > distances[current] + 1:
                distances[c] = distances[current] + 1
                from_[c] = current

        unvisited.remove(current)

        if all(distances[n] == math.inf for n in unvisited):
            path = []
            if type(destination) is list:
                destination = sorted(
                    (k for k in distances.keys() if k in destination),
                    key=lambda k: distances[k],
                )[0]
            prev = destination
            while prev:
                path.append(prev)
                prev = from_[prev]
            return list(reversed(path))

        current = sorted(unvisited, key=lambda n: distances[n])[0]


def print_path(path):
    width = max(col for _, col in path) + 1
    height = max(row for row, _ in path) + 1
    diagram = []
    for _ in range(height):
        diagram.append(["."] * width)

    for step, n in pairwise(path):
        row, col = step
        nrow, ncol = n
        direction = (nrow - row, ncol - col)
        if direction == (-1, 0):
            diagram[row][col] = "^"
        elif direction == (1, 0):
            diagram[row][col] = "v"
        elif direction == (0, -1):
            diagram[row][col] = "<"
        elif direction == (0, 1):
            diagram[row][col] = ">"
        else:
            print("dir", direction)

    row, col = path[-1]
    diagram[row][col] = "E"

    print("\n".join("".join(map(str, l)) for l in diagram))


with fileinput.input() as f:
    start, end = None, None
    starts = [start]

    for row, (rank, below) in enumerate(
        pairwise(chain((l for l in f), [None]))
    ):
        for col, (s, s_next) in enumerate(pairwise(chain(rank, [None]))):
            if can_jump(s, s_next):
                neighbors[(row, col)].append((row, col + 1))
                reverse_neighbors[(row, col + 1)].append((row, col))
            if can_jump(s_next, s):
                neighbors[(row, col + 1)].append((row, col))
                reverse_neighbors[(row, col)].append((row, col + 1))
            if below and can_jump(s, below[col]):
                neighbors[(row, col)].append((row + 1, col))
                reverse_neighbors[(row + 1, col)].append((row, col))
            if below and can_jump(below[col], s):
                neighbors[(row + 1, col)].append((row, col))
                reverse_neighbors[(row, col)].append((row + 1, col))

            if s == "S":
                start = (row, col)
            elif s == "E":
                end = (row, col)
            elif s == "a":
                starts.append((row, col))

    path = find_path(neighbors, start, end)
    # print_path(path)
    print(len(path) - 1)

    path = find_path(reverse_neighbors, end, starts)
    # print_path(path[::-1])
    print(len(path) - 1)
