import fileinput
from itertools import chain, repeat

DIRECTIONS = {
    "U": complex(0, -1),
    "D": complex(0, 1),
    "L": complex(-1, 0),
    "R": complex(1, 0),
}


def show_positions(positions):
    width = int(max(abs(p.real) for p in positions))
    height = int(max(abs(p.imag) for p in positions))

    for y in range(-height - 1, height + 1):
        for x in range(-width - 2, width + 2):
            if complex(x, y) in positions:
                if type(positions) is list:
                    idx = positions.index(complex(x, y))
                    print(idx if idx != 0 else "H", end="")
                else:
                    print("#", end="")
            elif x == 0 and y == 0:
                print("s", end="")
            else:
                print(".", end="")
        print()
    print("-" * (width * 2 + 2))


def move(head, tail, direction):
    if head + direction == tail:
        return tail, tail
    elif abs(head + direction - tail) <= 2**0.5:
        return head + direction, tail
    elif abs(tail - head) == 2:
        return head + direction, tail + direction
    else:
        destination = head + direction - tail

        return head + direction, tail + complex(
            destination.real / abs(destination.real)
            if destination.real != 0
            else 0,
            destination.imag / abs(destination.imag)
            if destination.imag != 0
            else 0,
        )


instructions = chain.from_iterable(
    repeat(DIRECTIONS[m], int(n))
    for m, n in (l.split() for l in fileinput.input())
)


rope = (complex(),) * 10
tails = {rope[-1]}

for direction in instructions:
    new_rope = []
    head = rope[0]

    for tail in rope[1:]:
        h, t = move(head, tail, direction)
        new_rope.append(h)
        direction = t - tail
        head = tail
    new_rope.append(t)

    tails.add(new_rope[-1])
    rope = new_rope

# show_positions(tails)

print(len(tails))
