from typing import Literal

from src.schemes.base import StrictBaseModel


class _League(StrictBaseModel):
    seasonAVG_overall: float
    seasonBTTSPercentage: int
    seasonOver25Percentage_overall: int
    progress: int
    id: int

    name: str
    name_jp: str | None
    name_tr: str | None
    name_kr: str | None
    name_ru: str | None
    name_es: str | None
    country: str | None

    domestic_scale: int
    international_scale: int
    status: str  # Literal["In Progress"]
    division: int
    starting_year: int
    ending_year: int
    comp_master_id: int
    country_iso: str


class _TopLeagues(StrictBaseModel):
    title: Literal["BTTS Leagues"]
    list_type: Literal["leagues"]
    data: list[_League]


class _Fixture(StrictBaseModel):
    id: int
    avg_potential: float
    date_unix: int
    btts_potential: int
    odds_btts_yes: float
    o25_potential: int
    home_name: str
    away_name: str
    country: str
    name: str
    progress: int
    country_iso: str
    next_match_id: int


class _TopFixtures(StrictBaseModel):
    title: Literal["BTTS Fixtures"]
    list_type: Literal["fixtures"]
    data: list[_Fixture]


class _Team(StrictBaseModel):
    seasonBTTS_overall: int
    seasonMatchesPlayed_overall: int
    seasonBTTSPercentage_overall: int
    id: int
    country: str
    name: str
    full_name: str
    name_jp: str | None
    name_tr: str | None
    name_kr: str | None
    name_pt: str | None
    name_ru: str | None
    name_es: str | None

    next_match_id: int
    next_match_date: int
    next_match_team: str
    odds_btts_yes: float
    country_iso: str


class _TopTeams(StrictBaseModel):
    title: Literal["BTTS Teams"]
    list_type: Literal["teams"]
    data: list[_Team]


class BttsStats(StrictBaseModel):
    top_leagues: _TopLeagues
    top_fixtures: _TopFixtures
    top_teams: _TopTeams
