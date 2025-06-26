from typing import Annotated, Literal

from pydantic import HttpUrl

from .base import StrictBaseModel, validate_season_year
from .team_stats import TeamStats


class Team(StrictBaseModel):
    stats: TeamStats

    id: int
    continent: str | None
    image: HttpUrl
    season: Annotated[str, validate_season_year]
    url: HttpUrl
    table_position: int
    performance_rank: int
    risk: int
    season_format: Literal["Cup", "Domestic League", "International"]
    competition_id: int
    founded: Annotated[str, validate_season_year]
    country: str
    name: str
    full_name: str
    english_name: str
    alt_names: list[str]
    official_sites: list[HttpUrl]
    stadium_name: str | None = None
    stadium_address: str | None = None
