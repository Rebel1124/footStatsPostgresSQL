from typing import Annotated, Literal

from pydantic import HttpUrl, StringConstraints

from .base import StrContinentCode, StrictBaseModel, validate_season_year


class LeagueReferee(StrictBaseModel):
    id: int
    competition_id: int
    full_name: str
    first_name: str
    last_name: str
    known_as: str
    shorthand: str
    age: int
    league: str
    league_type: Literal["Domestic League", "Cup"]
    url: HttpUrl
    season: Annotated[str, validate_season_year]
    continent: StrContinentCode
    starting_year: int
    ending_year: int
    birthday: int
    nationality: Annotated[str, StringConstraints(strip_whitespace=True, to_lower=True)]
    appearances_overall: int
    wins_home: int
    wins_away: int
    draws_overall: int
    wins_per_home: int
    wins_per_away: int
    draws_per: int
    btts_overall: int
    btts_percentage: int
    goals_overall: int
    goals_home: int
    goals_away: int
    goals_per_match_overall: float
    goals_per_match_home: float
    goals_per_match_away: float
    penalties_given_overall: int
    penalties_given_home: int
    penalties_given_away: int
    penalties_given_per_match_overall: float
    penalties_given_per_match_home: float
    penalties_given_per_match_away: float
    penalties_given_percentage_overall: int
    penalties_given_percentage_home: int
    penalties_given_percentage_away: int
    cards_overall: int
    cards_home: int
    cards_away: int
    cards_per_match_overall: float
    cards_per_match_home: float
    cards_per_match_away: float
    over05_cards_overall: int
    over15_cards_overall: int
    over25_cards_overall: int
    over35_cards_overall: int
    over45_cards_overall: int
    over55_cards_overall: int
    over65_cards_overall: int
    over05_cards_per_match_overall: float
    over15_cards_per_match_overall: float
    over25_cards_per_match_overall: float
    over35_cards_per_match_overall: float
    over45_cards_per_match_overall: float
    over55_cards_per_match_overall: float
    over65_cards_per_match_overall: float
    over05_cards_percentage_overall: int
    over15_cards_percentage_overall: int
    over25_cards_percentage_overall: int
    over35_cards_percentage_overall: int
    over45_cards_percentage_overall: int
    over55_cards_percentage_overall: int
    over65_cards_percentage_overall: int
    yellow_cards_overall: int
    red_cards_overall: int
    min_per_goal_overall: int
    min_per_card_overall: int
