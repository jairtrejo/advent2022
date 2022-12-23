import fileinput
from functools import cmp_to_key
from itertools import chain, dropwhile, groupby


def compare(left, right):
    if type(left) is int and type(right) is int:
        return right - left

    elif type(left) is list and type(right) is list:
        comparison = next(
            dropwhile(
                lambda c: c == 0, (compare(l, r) for l, r in zip(left, right))
            ),
            None,
        )
        if comparison:
            return comparison
        else:
            return len(right) - len(left)

    elif type(left) is int:
        return compare([left], right)

    elif type(right) is int:
        return compare(left, [right])

    else:
        raise ValueError()


with fileinput.input() as f:
    pairs = [
        tuple(map(lambda s: eval(s.strip()), g))
        for k, g in groupby((l for l in f), lambda l: l != "\n")
        if k
    ]

    print(
        sum(
            i + 1
            for i, (left, right) in enumerate(pairs)
            if compare(left, right) > 0
        )
    )

    packets = [
        packet
        for packet in sorted(
            chain(*pairs, [[[2]], [[6]]]),
            key=cmp_to_key(compare),
            reverse=True,
        )
    ]

    print((packets.index([[2]]) + 1) * (packets.index([[6]]) + 1))
