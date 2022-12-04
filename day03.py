import fileinput
import string
from itertools import tee

PRIORITIES = {
    **{l: ord(l) - ord("a") + 1 for l in string.ascii_lowercase},
    **{l: ord(l) - ord("A") + 27 for l in string.ascii_uppercase},
}


def main():
    with fileinput.input() as f:
        rucksacks = (
            (
                set(rucksack[: len(rucksack) >> 1]),
                set(rucksack[len(rucksack) >> 1 :]),
            )
            for rucksack in (line.strip() for line in f)
        )

        part_one, part_two = tee(rucksacks)

        mistakes = (next(iter(a & b)) for a, b in part_one)
        print(sum(PRIORITIES[mistake] for mistake in mistakes))

        elf_groups = zip(*([(a | b for a, b in part_two)] * 3))
        badges = (next(iter(a & b & c)) for a, b, c in elf_groups)
        print(sum(PRIORITIES[badge] for badge in badges))


if __name__ == "__main__":
    main()
