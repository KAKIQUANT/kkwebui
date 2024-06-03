
from pathlib import Path

WORKDIR = Path(__file__).parent

DATA_DIR = WORKDIR.joinpath("data")
print(DATA_DIR)
DATA_DIR_QUOTES = DATA_DIR.joinpath('quotes')
DATA_DIR_CSVS = DATA_DIR.joinpath('csvs')
dirs = [DATA_DIR, DATA_DIR_QUOTES, DATA_DIR_CSVS]

for dir in dirs:
    dir.mkdir(exist_ok=True, parents=True)
