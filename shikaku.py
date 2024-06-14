# pyright: basic
from collections import defaultdict
from typing import Optional
from itertools import batched, product
import pprint as pp
from parse import shikaku_from_json, Shikaku, Position
import fetch


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

    # COLORS = "ABCDEFGHIJKLMNOPQ"
    COLORS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQ!@#$%^&*"

    nums = []
    grid_orig = [x[:] for x in grid]

    N = len(grid)
    for x in range(N):
        for y in range(N):
            if grid[x][y].isdigit():
                d = int(grid[x][y])
                nums.append((x, y, d, fac[d]))

    class fg:
        reset = "\033[0m"
        black = "\033[30m"
        red = "\033[31m"
        green = "\033[32m"
        orange = "\033[33m"
        blue = "\033[34m"
        purple = "\033[35m"
        cyan = "\033[36m"
        lightgrey = "\033[37m"
        darkgrey = "\033[90m"
        lightred = "\033[91m"
        lightgreen = "\033[92m"
        yellow = "\033[93m"
        lightblue = "\033[94m"
        pink = "\033[95m"
        lightcyan = "\033[96m"

    REAL_COLORS = [
        fg.green,
        fg.orange,
        fg.blue,
        fg.purple,
        fg.cyan,
        fg.lightred,
        fg.lightgreen,
        fg.yellow,
        fg.lightblue,
        fg.pink,
        fg.lightcyan,
    ]

    def pprint(grid):
        c: defaultdict[str, Optional[str]] = defaultdict(lambda: None)
        c["X"] = fg.black

        i = 0
        for line in grid:
            for char in line:
                if char.isdigit():
                    print(char, end="")
                    continue

                if v := c[char]:
                    print(v, end="")
                else:
                    c[char] = REAL_COLORS[i % len(REAL_COLORS)]
                    i += 1
                    print(c[char], end="")

                # print("█", end="")
                print(char, end="")
                print(fg.reset, end="")

            print()

        print(fg.reset)
        # print("\n".join(["".join(x) for x in grid]))

    def fill(orig, x, y, w, h, c):
        grid = [r.copy() for r in orig]

        for ox in range(w):
            for oy in range(h):
                sx, sy = x + ox, y + oy
                grid[sx][sy] = c

        return grid

    def check(grid, x: int, y: int, w: int, h: int, n: int) -> bool:
        s = str(n)
        for u in range(x, x + w):
            for v in range(y, y + h):
                g = grid[u][v]
                if g != "X" and g != s:
                    return False

        return True

    def _check(grid, x: int, y: int, w: int, h: int, n: int) -> bool:
        if (not 0 <= x < N) or (not 0 <= y < N):
            return False

        if (not x + w <= N) or (not y + h <= N):
            return False

        for u in range(x, x + w):
            for v in range(y, y + h):
                c = grid_orig[u][v]

                if c.isdigit() and c != str(n):
                    return False

                if grid[u][v] not in ["X", str(n)]:
                    return False

        return True
        # if (d := grid_orig[x][y]).isdigit() and int(d) != n:
        #     return False

    def solve(grid, i):
        if i == len(nums):
            print("FOUND SOLUTION")
            pprint(grid)
            # print("\n".join(["".join(x) for x in grid]))
            # exit(0)

            return grid

        # print(i)
        # print('-'*30)
        # pprint(grid)
        # print('-'*30)
        n, f = nums[i]

        for x, y, w, h in f:
            if not check(grid, x, y, w, h, n):
                continue

            # pprint(grid)

            if r := solve(fill(grid, x, y, w, h, COLORS[i % len(COLORS)]), i + 1):
                print(f"{x=}, {y=}, {w=}, {h=}, {n=} -> {(n, None) = }")
                pprint(grid)
                return r

        return None


    def prune(orig):
        num = []
        for x, y, n, f in orig:
            real = []
            for w, h in f:
                for ox, oy in product(range(w), range(h)):
                    sx, sy = x - ox, y - oy
                    if not _check(grid, sx, sy, w, h, n):
                        continue

                    real.append((sx, sy, w, h))

            real = list(set(real))
            num.append((n, real))

        return num

    nums = sorted(
        prune(nums), key=lambda x: x[0] + 100000 * int(len(x[1]) == 1), reverse=True
    )

    pp.pprint(nums)

    res = solve(grid, 0)

    if res is not None:
        pprint(res)
    else:
        print("no sol")


problem = """
    X2X2X
    3X51X
    X1X34
    X4XXX
    XXXXX
""".strip()

cells = shikaku_from_json("./master.json", 40)
# cells = fetch.today('expert')
grid = [list(x) for x in batched(cells, 40)]

solution(grid)
