import fileinput
import re
from collections import deque
from itertools import groupby


class Monkey:
    def __init__(self, items, operation, criterion):
        self.inspections = 0
        self.items = deque(items)

        self.operation = operation
        self.criterion = criterion
        self.monkey_a = None
        self.monkey_b = None
        self.calm_factor = 1

    def inspect(self):
        self.inspections += 1
        item = self.items.popleft()
        # print(f"\tMonkey inspects an item with a worry level of {item}")
        new_item = eval(self.operation, {}, {"old": item})
        # print(f"\t\tWorry level is {self.operation} to {new_item}")
        # new_item = int(new_item // 3)
        new_item = new_item % calm_factor
        # print(f"\t\tWorry level is divided by 3 to {new_item}")
        return new_item

    def throw(self, item):
        if item % self.criterion == 0:
            # print(f"\t\tCurrent worry level is divisible by {self.criterion}")
            self.monkey_a.catch(item)
        else:
            # print(
            # f"\t\tCurrent worry level is not divisible by {self.criterion}"
            # )
            self.monkey_b.catch(item)

    def catch(self, item):
        self.items.append(item)

    def turn(self):
        while len(self.items) > 0:
            item = self.inspect()
            self.throw(item)

    def __repr__(self):
        return (
            f"<Monkey: inspections: {self.inspections}, items: {self.items}>"
        )

    def from_input(lines):
        next(lines)  # header
        items = [
            int(worry)
            for worry in re.match(
                r"^\s+Starting items: (?P<items>.+)$", next(lines)
            )
            .group("items")
            .split(",")
        ]

        operation = re.match(
            "^\s+Operation: new = (?P<operation>.+)", next(lines)
        ).group("operation")

        criterion = int(
            re.match(
                r"^\s+Test: divisible by (?P<criterion>\d+)\s+$", next(lines)
            ).group("criterion")
        )

        m = Monkey(items, operation, criterion)
        return m


with fileinput.input() as f:
    monkeys = []
    relationships = {}
    calm_factor = 1
    for k, lines in groupby((l for l in f), lambda l: l != "\n"):
        if not k:
            continue
        monkey = Monkey.from_input(lines)
        monkeys.append(monkey)

        monkey_a = int(next(lines).split(" ")[-1])
        monkey_b = int(next(lines).split(" ")[-1])
        relationships[monkey] = (monkey_a, monkey_b)

        calm_factor *= monkey.criterion

    for monkey, (monkey_a, monkey_b) in relationships.items():
        monkey.monkey_a = monkeys[monkey_a]
        monkey.monkey_b = monkeys[monkey_b]

    for monkey in monkeys:
        monkey.calm_factor = calm_factor

    for _ in range(10000):
        for i, monkey in enumerate(monkeys):
            # print(f"Monkey {i}:")
            monkey.turn()

    first, second = sorted(monkeys, key=lambda m: m.inspections, reverse=True)[
        :2
    ]
    print(first.inspections * second.inspections)
    print(
        "\n".join(
            f"Monkey {i}: {m.inspections}" for i, m in enumerate(monkeys)
        )
    )
