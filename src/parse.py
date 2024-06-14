from pydantic import BaseModel, TypeAdapter
from itertools import batched

class Position(BaseModel):
    index: int
    number: int


Shikaku = TypeAdapter(list[Position])


def shikaku_from_json(fname: str, size: int) -> list[str]:
    with open(fname, "r") as f:
        s = f.read()

        locs = Shikaku.validate_json(s)

    board = ["X"] * (size**2)

    for loc in locs:
        board[loc.index] = str(loc.number)

    return board


if __name__ == "__main__":
    b = batched(shikaku_from_json("./hard_master.json", 40), 40)
    print('\n'.join(' '.join(x) for x in b).replace('X', '0'))
