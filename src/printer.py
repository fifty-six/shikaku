# pyright: basic
from collections import defaultdict
from typing import Optional

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
                if len(char)  == 1:
                    print(char, end="")
                else:
                    print("#", end="")
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

