import fileinput
from collections import defaultdict, namedtuple

Tree = namedtuple("Tree", "height row col")


def add_to_front(visible, tree):
    """
    A tree at the front:
    - is always visible and,
    - it hides shorter trees.
    """
    return [tree, *(t for t in visible if t.height > tree.height)]


def add_to_back(visible, tree):
    """
    A tree at the back:
    - is only visible if tall enough and,
    - it can't hide other trees.
    """
    if all((t.height < tree.height for t in visible)):
        return [*visible, tree]
    else:
        return visible


scores = defaultdict(lambda: (0,) * 4)
rows = []
cols = []
i = 0
with fileinput.input() as f:
    for row, l in enumerate(l for l in f):
        rows.append((set(), set()))
        for col, h in enumerate(l.strip()):
            if row == 0:
                cols.append((set(), set()))

            top, bottom = cols[col]
            left, right = rows[row]

            tree = Tree(int(h), row, col)

            # Backwards score
            _, b, _, r = scores[tree]
            t = row - next(
                (t.row for t in bottom if t.height >= tree.height),
                0,
            )
            l = col - next(
                (t.col for t in right if t.height >= tree.height),
                0,
            )
            scores[tree] = (t, b, l, r)

            # Forwards score
            for v in bottom:
                t, b, l, r = scores[v]
                scores[v] = (t, b + 1, l, r)

            for v in right:
                t, b, l, r = scores[v]
                scores[v] = (t, b, l, r + 1)

            top = add_to_back(top, tree)
            bottom = add_to_front(bottom, tree)
            left = add_to_back(left, tree)
            right = add_to_front(right, tree)

            cols[col] = (top, bottom)
            rows[row] = (left, right)

all_visible = set()

for forwards, backwards in cols + rows:
    all_visible |= set(forwards)
    all_visible |= set(backwards)

print(len(all_visible))
print(max(t * b * l * r for t, b, l, r in scores.values()))
