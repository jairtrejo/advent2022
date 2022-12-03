import fileinput
from functools import reduce
from itertools import groupby


def main():
    elves = (
        sum(int(calories) for calories in elf if calories != "\n")
        for _, elf in groupby(
            (l for l in fileinput.input()), lambda l: l == "\n"
        )
        if elf != ["\n"]
    )

    top_three = reduce(
        lambda top, v: sorted([*top, v], reverse=True)[:3], elves, []
    )

    print(top_three[0])
    print(sum(top_three))


if __name__ == "__main__":
    main()
