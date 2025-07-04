from typing import Annotated

from pydantic import HttpUrl

from .base import StrictBaseModel, validate_season_year
from .team_stats import TeamStats


class _TeamStatsLastX(TeamStats):
    last_x: int


class TeamLastX(StrictBaseModel):
    stats: _TeamStatsLastX

    last_updated_match_timestamp: int
    last_x_home_away_or_overall: int
    last_x_match_num: int
    id: int
    continent: str | None
    image: HttpUrl
    season: Annotated[str, validate_season_year]
    url: HttpUrl
    table_position: int
    performance_rank: int
    risk: int
    season_format: str  # Literal["Cup", "Domestic League", "International"]
    competition_id: int
    founded: Annotated[str, validate_season_year]
    country: str
    name: str
    full_name: str
    english_name: str
    alt_names: list[str]
    official_sites: list[HttpUrl]
