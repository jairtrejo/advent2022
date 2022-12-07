import fileinput
from collections import defaultdict

with fileinput.input() as f:
    tree = defaultdict(dict)
    current_dir = []

    for l in f:
        if l.startswith("$ cd /"):
            current_dir = ["/"]
        elif l.startswith("$ cd .."):
            current_dir.pop()
        elif l.startswith("$ cd"):
            go_to = l[5:].strip()
            current_dir.append(go_to)
        elif l.startswith("$ ls"):
            pass
        else:
            size, filename = l.strip().split(" ")
            if size == "dir":
                pass
            else:
                for i, d in enumerate(current_dir):
                    tree["/".join(current_dir[: i + 1])][
                        "/".join([*current_dir[i:], filename])
                    ] = int(size)

    print(
        "Part one:",
        sum(
            size
            for size in (sum(sizes.values()) for sizes in tree.values())
            if size <= 100000
        ),
    )

    root = sum(tree["/"].values())
    needed = 30000000 - (70000000 - root)

    print(
        "Part two:",
        next(
            size
            for size in sorted(sum(sizes.values()) for sizes in tree.values())
            if size >= needed
        ),
    )
