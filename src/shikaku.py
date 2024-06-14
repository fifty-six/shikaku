#!/usr/bin/python

# pyright: basic
from collections import defaultdict
from typing import Optional
from itertools import batched, product
import itertools
import pprint as pp
from parse import shikaku_from_json
import fetch
from printer import pprint

Possibility = tuple[int, int, int, int]
Coord = tuple[int, int]


def solution(grid: list[list[str]]):
    print(grid)
    fac: defaultdict[int, list] = defaultdict(list)

    def valid_sizes(X):
        for i in range(1, X + 1):
            q, r = divmod(X, i)

            if r != 0:
                continue

            yield (q, i)

    print(list(valid_sizes(24)))
    for x in range(1, 500 + 1):
        fac[x] = list(valid_sizes(x))

    COLORS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQ!@$%^&*"

    nums = []
    grid_orig = [x[:] for x in grid]

    N = len(grid)
    for x in range(N):
        for y in range(N):
            if grid[x][y].isdigit():
                d = int(grid[x][y])
                nums.append((x, y, d, fac[d]))

    def rect(x0, y0, w, h):
        for x in range(x0, x0 + w):
            for y in range(y0, y0 + h):
                yield (x, y)

    def fill(orig, pos, c):
        grid = [r.copy() for r in orig]

        for x, y in rect(*pos):
            grid[x][y] = c

        return grid

    def _check(grid, x: int, y: int, w: int, h: int, n: int) -> bool:
        if (not 0 <= x < N) or (not 0 <= y < N):
            return False

        if (not x + w <= N) or (not y + h <= N):
            return False

        for u, v in rect(x, y, w, h):
            c = grid_orig[u][v]

            if c.isdigit() and c != str(n):
                return False

            if grid[u][v] not in ["X", str(n)]:
                return False

        return True

    def solve(i, impossible):
        if i == len(nums):
            return grid

        n, f = nums[i]

        for pos in f - impossible:
            removed = overlaps[pos]

            if r := solve(
                i + 1,
                impossible | removed,
            ):
                return fill(r, pos, COLORS[i % len(COLORS)])

        return None

    possibilities: defaultdict[Coord, set[tuple[int, Possibility]]] = defaultdict(set)
    cover: defaultdict[Coord, set[Possibility]] = defaultdict(set)

    def add_cover(pos: Possibility, num: int):
        for u, v in rect(*pos):
            cover[(u, v)].add(pos)

    def process(orig):
        nums: list[tuple[int, set[Possibility]]] = []

        for x, y, num, facs in orig:
            real = set()
            for w, h in facs:
                for ox, oy in product(range(w), range(h)):
                    sx, sy = x - ox, y - oy

                    if not _check(grid, sx, sy, w, h, num):
                        continue

                    pos: Possibility = (sx, sy, w, h)

                    real.add(pos)
                    possibilities[(sx, sy)].add((num, pos))
                    add_cover(pos, num)

            nums.append((num, real))

        return nums

    def find_overlaps():
        invalidates: defaultdict[Possibility, set[Possibility]] = defaultdict(set)

        # so, we now have the coverings. what I *want* is to
        # remove, after each iter, the ones each placement invalidates
        for vs in possibilities.values():
            # So, for each possible placement, at every coordinate,
            for num, pos in vs:
                # We go over the grid and see anything it'd hit if placed
                invalidates[pos] = set(
                    itertools.chain.from_iterable(
                        cover[(u, v)] for (u, v) in rect(*pos)
                    )
                )

        return invalidates

    import time

    start_time = time.time()
    pruned = process(nums)
    overlaps = find_overlaps()
    print("--- %s seconds ---" % (time.time() - start_time))

    nums = sorted(
        pruned,
        key=lambda x: (x[0] + 100000 * int(len(x[1]) == 1), -len(x[1])),
        reverse=True,
    )

    # pp.pprint(nums)
    if r := solve(0, set()):
        pprint(r)
    else:
        print(":(")


size = 40
cells = shikaku_from_json("./master.json", size)
# cells = fetch.today('expert')
grid = [list(x) for x in batched(cells, size)]

solution(grid)
