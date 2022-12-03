import fileinput

BEATS = {
    "A": "Z",
    "C": "Y",
    "B": "X",
    "X": "C",
    "Z": "B",
    "Y": "A",
}


def round(opponent, me):
    shape_score = ord(me) - ord("X") + 1

    if BEATS[me] == opponent:
        outcome_score = 6
    elif BEATS[opponent] == me:
        outcome_score = 0
    else:
        outcome_score = 3

    return shape_score + outcome_score


def play(result, opponent):
    if result == "X":
        me = BEATS[opponent]
    elif result == "Y":
        me = chr(ord(opponent) - ord("A") + ord("X"))
    elif result == "Z":
        me = next(me for me, other in BEATS.items() if other == opponent)

    return me


def main():
    with fileinput.input() as f:
        print(
            sum(
                round(opponent, me)
                for opponent, me in (line.split() for line in f)
            )
        )

    with fileinput.input() as f:
        print(
            sum(
                round(opponent, play(result, opponent))
                for opponent, result in (line.split() for line in f)
            )
        )


if __name__ == "__main__":
    main()
