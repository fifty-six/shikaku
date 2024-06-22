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
from sys import argv

Possibility = tuple[int, int, int, int]
Coord = tuple[int, int]
Num = int


def valid_sizes(X):
    for i in range(1, X + 1):
        q, r = divmod(X, i)

        if r != 0:
            continue

        yield (q, i)


def rect(x0, y0, w, h):
    for x in range(x0, x0 + w):
        for y in range(y0, y0 + h):
            yield (x, y)


def fill(orig, pos, c):
    grid = [r.copy() for r in orig]

    for x, y in rect(*pos):
        grid[x][y] = c

    return grid


COLORS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQ!@$%^&*"


class Solution:
    def __init__(self, grid: list[list[str]]):
        print(grid)
        fac: defaultdict[int, list] = defaultdict(list)

        print(list(valid_sizes(24)))
        for x in range(1, 500 + 1):
            fac[x] = list(valid_sizes(x))

        nums = []
        self.grid = grid

        self.N = N = len(grid)

        for x in range(N):
            for y in range(N):
                if grid[x][y].isdigit():
                    d = int(grid[x][y])
                    nums.append((x, y, d, fac[d]))

        self.possibilities: defaultdict[Coord, set[tuple[Num, Possibility]]] = (
            defaultdict(set)
        )
        self.cover: defaultdict[Coord, set[Possibility]] = defaultdict(set)

        import time

        start_time = time.time()
        processed = self.process(nums)
        self.overlaps = self.find_overlaps()
        print("--- %s seconds ---" % (time.time() - start_time))

        self.nums = sorted(
            processed,
            key=self.heur
        )

    @staticmethod
    def heur(p: tuple[Num, set[Possibility]]):
        num, possibilities = p

        area_score = num

        # cheat if it's only one possible
        if len(possibilities) <= 1:
            area_score = 100000

        # Sort by bigger area first, then those with less possibilities.
        return (area_score, -len(possibilities))

    def solve(self):
        return self._solve(0)#, set())

    def solve_and_print(self):
        if r := self.solve():
            pprint(r)
        else:
            print(":(")

    def _check(self, x: int, y: int, w: int, h: int, n: int) -> bool:
        if (not 0 <= x < self.N) or (not 0 <= y < self.N):
            return False

        if (not x + w <= self.N) or (not y + h <= self.N):
            return False

        for u, v in rect(x, y, w, h):
            c = self.grid[u][v]

            if c.isdigit() and c != str(n):
                return False

            if self.grid[u][v] not in ["X", str(n)]:
                return False

        return True

    def _solve(self, i):
        if len(self.nums) == 0:
            return grid

        n, f = self.nums.pop()

        old = self.nums

        for pos in f:
            removed = self.overlaps[pos]

            self.nums = sorted([(num, ps - removed) for (num, ps) in self.nums], key=self.heur)

            if r := self._solve(
                i + 1,
            ):
                return fill(r, pos, COLORS[i % len(COLORS)])

            self.nums = old
        
        return None

    def add_cover(self, pos: Possibility, num: int):
        for u, v in rect(*pos):
            self.cover[(u, v)].add(pos)

    # This does unfathomable amounts of bullshit
    def process(self, orig):
        nums: list[tuple[int, set[Possibility]]] = []

        for x, y, num, facs in orig:
            real = set()
            for w, h in facs:
                for ox, oy in product(range(w), range(h)):
                    sx, sy = x - ox, y - oy

                    if not self._check(sx, sy, w, h, num):
                        continue

                    pos: Possibility = (sx, sy, w, h)

                    real.add(pos)
                    self.possibilities[(sx, sy)].add((num, pos))
                    self.add_cover(pos, num)

            nums.append((num, real))

        return nums

    def find_overlaps(self):
        invalidates: defaultdict[Possibility, set[Possibility]] = defaultdict(set)

        # so, we now have the coverings. what I *want* is to
        # remove, after each iter, the ones each placement invalidates
        for vs in self.possibilities.values():
            # So, for each possible placement, at every coordinate,
            for num, pos in vs:
                # We go over the grid and see anything it'd hit if placed
                invalidates[pos] = set(
                    itertools.chain.from_iterable(
                        self.cover[(u, v)] for (u, v) in rect(*pos)
                    )
                )

        return invalidates

if len(argv) != 2:
    print(f"Usage: {argv[0]} [FILE]")
    exit(-1)

size = 40
cells = shikaku_from_json(argv[1], size)
# cells = fetch.today('expert')
grid = [list(x) for x in batched(cells, size)]

sol = Solution(grid)
sol.solve_and_print()
