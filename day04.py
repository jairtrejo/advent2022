import fileinput
import re
from itertools import tee

gen_pairs = lambda f: (
    ((a, b), (c, d))
    for a, b, c, d in (map(int, re.split(r"[,-]", l)) for l in f)
)

gen_overlaps = lambda pairs: (
    max(min(b, d) - max(a, c) + 1, 0) for ((a, b), (c, d)) in pairs
)

with fileinput.input() as f:
    pairs = gen_pairs(f)
    overlaps = gen_overlaps(pairs)
    print(sum(1 for o in overlaps if o > 0))

with fileinput.input() as f:
    pairs, pairs_prime = tee(gen_pairs(f))
    print(
        sum(
            1
            for o, ((a, b), (c, d)) in zip(gen_overlaps(pairs), pairs_prime)
            if o == b - a + 1 or o == d - c + 1
        )
    )
