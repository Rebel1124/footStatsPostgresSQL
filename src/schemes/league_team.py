from typing import Annotated, Literal

from pydantic import HttpUrl

from .base import (
    StrictBaseModel,
    empty_str_to_none,
    validate_event_times,
    validate_season_year,
)
from .team_stats import TeamStats


class _LeagueTeamStats(TeamStats):  # Extended stats
    gd_text_2hg_away: Annotated[float | None, empty_str_to_none]
    seasonGoals_home: Annotated[list[str], validate_event_times]
    seasonGoals_away: Annotated[list[str], validate_event_times]
    formRun_2hg_home: Annotated[int | None, empty_str_to_none]
    currentFormAway: int | None
    formRun_2hg_overall: Annotated[int | None, empty_str_to_none]
    seasonConceded_away: Annotated[list[str], validate_event_times]
    seasonRecentPPG: float | None
    formRun_ht_home: Annotated[int | None, empty_str_to_none]
    previous_seasons: list[int]
    gd_text_2hg_home: Annotated[float | None, empty_str_to_none]
    formRun_ht_away: Annotated[int | None, empty_str_to_none]
    gd_text_2hg_overall: Annotated[int | None, empty_str_to_none]
    ppg_2hg_processed_away: Annotated[float | None, empty_str_to_none]
    ppg_2hg_processed_overall: Annotated[float | None, empty_str_to_none]
    formRun_ht_overall: Annotated[int | None, empty_str_to_none]
    seasonConceded_home: Annotated[list[str], validate_event_times]
    ppg_2hg_processed_home: Annotated[float | None, empty_str_to_none]
    currentFormHome: int | None
    formRun_2hg_away: Annotated[int | None, empty_str_to_none]


class LeagueTeam(StrictBaseModel):
    id: int
    name: str
    cleanName: str
    english_name: str
    shortHand: str
    country: str
    continent: None
    founded: Annotated[str, validate_season_year]
    image: HttpUrl
    flag_element: None
    season: Annotated[str, validate_season_year]
    seasonClean: None
    url: HttpUrl
    table_position: int
    performance_rank: int
    risk: int
    season_format: Literal["Domestic League", "Cup"]
    competition_id: int
    full_name: str
    alt_names: list[str]
    official_sites: list[HttpUrl]
    stats: _LeagueTeamStats
