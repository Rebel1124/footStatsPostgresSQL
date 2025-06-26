from datetime import datetime

from pydantic import BaseModel

from src.schemes import (
    LeagueMatch,
    LeaguePlayer,
    LeagueReferee,
    LeagueStats,
    LeagueTeam,
)
from src.schemes.base import StrSeasonYear
from src.schemes.league_tables import LeagueTables


class SeasonMetaData(BaseModel):
    season_id: int
    season_year: StrSeasonYear
    league_name: str


class Season(BaseModel):
    season_id: int
    season_year: StrSeasonYear
    league_name: str

    league_stats: LeagueStats
    league_matches: list[LeagueMatch]
    league_teams: list[LeagueTeam]
    league_players: list[LeaguePlayer]
    league_referees: list[LeagueReferee]
    league_tables: LeagueTables


class SeasonWithUpdateAt(Season):
    updated_at: datetime
