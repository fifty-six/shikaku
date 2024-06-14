

from typing import Literal
import bs4
import requests

Difficulty = Literal['master'] | Literal['hard'] | Literal['expert'] | Literal['easy'] | Literal['medium']

sizes = {
    'easy': 10,
    'hard': 20,
    'expert': 30,
    'master': 40,
}

def today(difficulty: Difficulty):
    # grid = /html/body/div/div[1]/div/div/div[3]/div[1]/div[2]
    txt = requests.get(f'https://shikakuofthe.day/{difficulty}').text
    soup = bs4.BeautifulSoup(txt, 'html5lib')

    # .overlay svelte-c5s5x5
    # > cell [same svelte class]
    cells = soup.select('.overlay')[0]
    cells = ['X' if x.text == ' ' else x.text.strip() for x in cells]

    # ??????
    _ = cells.pop()

    return cells
