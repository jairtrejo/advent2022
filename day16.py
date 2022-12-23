import fileinput
import math
import re
from functools import cache
from itertools import combinations

PARSER = re.compile(
    r"Valve (?P<name>\w+).+rate=(?P<rate>\d+).+valves? (?P<tunnels>(\w+,? ?)+)"
)

valves = {}
openable = tuple()
distances = dict()


def shortest_paths(neighbors, origin):
    unvisited = {node for node in neighbors.keys() if node != origin}
    unvisited.add(origin)

    distances = {node: math.inf for node in neighbors.keys() if node != origin}
    distances[origin] = 0

    current = origin
    while True:
        candidates = [n for n in neighbors[current] if n in unvisited]
        for c in candidates:
            if distances[c] > distances[current] + 1:
                distances[c] = distances[current] + 1

        unvisited.remove(current)

        if all(distances[n] == math.inf for n in unvisited):
            return distances

        current = sorted(unvisited, key=lambda n: distances[n])[0]


@cache
def best_path(start, valves, time):
    if not valves:
        return 0

    if time <= 0:
        return 0

    best = 0

    for valve in valves:
        name, rate, _ = valve
        time_left = time - distances[start[0]][name] - 1
        best_pressure = rate * time_left + best_path(
            valve, tuple(v for v in valves if v != valve), time_left
        )
        if best_pressure > best:
            best = best_pressure

    return best


@cache
def best_path_with_elephant(start, valves, time):
    best = 0

    for n in range(1, len(valves)):
        for my_valves in combinations(valves, n):
            my_valves = frozenset(my_valves)
            el_valves = valves - my_valves
            total = best_path(start, tuple(my_valves), time) + best_path(
                start, tuple(el_valves), time
            )
            if total > best:
                best = total

    return best


with fileinput.input() as f:
    valves = {
        m.group("name"): (
            m.group("name"),
            int(m.group("rate")),
            tuple(m.group("tunnels").split(", ")),
        )
        for m in (PARSER.search(l) for l in f)
    }

    neighbors = {name: set(tunnels) for name, _, tunnels in valves.values()}

    distances = {
        name: shortest_paths(neighbors, name) for name in neighbors.keys()
    }

    openable = tuple(
        sorted(name for name, rate, _ in valves.values() if rate > 0)
    )

    print(best_path(valves["AA"], tuple(valves[o] for o in openable), 30))

    print(
        best_path_with_elephant(
            valves["AA"], frozenset(valves[o] for o in openable), 26
        )
    )
