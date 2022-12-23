import fileinput
import re
from itertools import pairwise


def manhattan(x0, y0, x1, y1):
    return abs(x1 - x0) + abs(y1 - y0)


def coverage(sensor, y):
    sx, sy, bx, by = sensor
    d = manhattan(sx, sy, bx, by)
    span = d - abs(y - sy)
    if span >= 0:
        return (sx - span, sx + span)
    else:
        return None


def dedupe(coverages):
    deduped = [coverages[0]]
    for coverage in coverages[1:]:
        pa, pb = deduped[-1]
        a, b = coverage
        if pa <= a <= (pb + 1):
            deduped[-1] = (pa, max(b, pb))
        else:
            deduped.append(coverage)
    return deduped


def find_gaps(coverages):
    return [(lb, ra) for (_, lb), (ra, _) in pairwise(coverages)]


with fileinput.input() as f:
    sensors = [
        tuple(
            map(
                int,
                (m.group("sx"), m.group("sy"), m.group("bx"), m.group("by")),
            )
        )
        for m in (
            re.search(
                r"x=(?P<sx>-?\d+), y=(?P<sy>-?\d+):.+x=(?P<bx>-?\d+), y=(?P<by>-?\d+)",
                l,
            )
            for l in f
        )
    ]

    y = 10

    coverages = sorted(
        filter(
            lambda c: c is not None,
            [coverage(sensor, y) for sensor in sensors],
        )
    )

    coverages = dedupe(coverages)

    print(sum(b - a for a, b in coverages))

    for y in range(4000000):
        coverages = sorted(
            filter(
                lambda c: c is not None,
                [coverage(sensor, y) for sensor in sensors],
            )
        )

        coverages = dedupe(coverages)
        gaps = find_gaps(coverages)
        if gaps:
            if len(gaps) > 1:
                raise Exception("Too many gaps")
            a, b = gaps[0]
            if (b - a) != 2:
                raise Exception("Gap too wide")
            print(4000000 * (a + 1) + y)
