import fileinput
import re
from itertools import tee

with fileinput.input() as f:
    pairs = (
        ((a, b), (c, d))
        for a, b, c, d in (map(int, re.split(r"[,-]", l)) for l in f)
    )
    overlaps = (
        (((a, b), (c, d)), max(min(b, d) - max(a, c) + 1, 0))
        for ((a, b), (c, d)) in pairs
    )

    overlaps, overlaps_p = tee(overlaps)

    print(sum(1 for _, o in overlaps if o > 0))

    print(
        sum(
            1
            for ((a, b), (c, d)), o in overlaps_p
            if o == b - a + 1 or o == d - c + 1
        )
    )
