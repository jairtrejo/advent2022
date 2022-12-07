import fileinput
import re
from itertools import chain, repeat

crates_re = re.compile(r"^((\s{3}|\[\w+\])\s?)+$")
instructions_re = re.compile(r"^move (\d+) from (\d+) to (\d+)\s$")
labels_re = re.compile(r"^(\s+\d)+\s+$")


with fileinput.input() as f:
    stacks = []

    for l in f:
        if crates_re.fullmatch(l):
            crates = [l[i + 1] for i in range(0, len(l), 4)]
            stacks = [
                [*stack, crate] if crate != " " else stack
                for stack, crate in zip(chain(stacks, repeat([])), crates)
            ]

        if m := instructions_re.fullmatch(l):
            n, origin, destination = map(int, m.groups())
            stacks[destination - 1] = (
                list(reversed(stacks[origin - 1][:n]))
                + stacks[destination - 1]
            )
            stacks[origin - 1] = stacks[origin - 1][n:]

    print("".join(stack[0] for stack in stacks))
