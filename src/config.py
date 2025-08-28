import os
from typing import Literal

from dotenv import load_dotenv

load_dotenv()

FOOTYSTATS_API_KEY = os.environ["FOOTYSTATS_API_KEY"]
DB_URL = os.environ["DB_URL"]

type LeagueName = Literal[
    "Germany Bundesliga",
    "Europe UEFA Champions League",
    "England Premier League",
    "England Championship",
    "Spain La Liga",
    "France Ligue 1",
    "Italy Serie A",
    "South Africa Premier Soccer League",
    "Europe UEFA Europa League",
    "South Africa National First Division",
]

LEAGUES_NAMES: list[LeagueName] = [
    "Germany Bundesliga",
    "Europe UEFA Champions League",
    "England Premier League",
    "England Championship",
    "Spain La Liga",
    "France Ligue 1",
    "Italy Serie A",
    "South Africa Premier Soccer League",
    "Europe UEFA Europa League",
    "South Africa National First Division",
]
