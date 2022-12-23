import fileinput
from itertools import tee


def register(instructions):
    x = 1
    yield x
    for i in instructions:
        if i is None:
            yield x
        else:
            yield x
            x += i
            yield x


with fileinput.input() as f:
    instructions = (
        int(l.split()[1]) if l.strip() != "noop" else None for l in f
    )

    part_one, part_two = tee(register(instructions))

    print(
        sum(
            x * (i + 1)
            for i, x in enumerate(part_one)
            if (i + 1) in (20, 60, 100, 140, 180, 220)
        )
    )

    for i, x in enumerate(part_two):
        row = i // 40
        col = i % 40
        if col == 0:
            print()
        print("#" if col in (x - 1, x, x + 1) else ".", end="")
    print()
