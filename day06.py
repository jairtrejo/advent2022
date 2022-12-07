import fileinput
import re
from itertools import islice

with fileinput.input() as f:
    for l in f:
        marker_start = lambda length: next(
            i + length
            for i, chord in enumerate(zip(*(l[n:] for n in range(length))))
            if len(set(chord)) == length
        )
        print(marker_start(4))
        print(marker_start(14))
