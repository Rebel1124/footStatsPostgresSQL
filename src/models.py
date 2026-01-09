from pydantic import AwareDatetime, BaseModel

from src.config import League
from src.scrapers import Bookmaker


class Odds1X2(BaseModel):
    home: float | None
    draw: float | None
    away: float | None


class AggregatedMatchOdds(BaseModel):
    actual_at: AwareDatetime
    start_at: AwareDatetime
    home_team: str
    away_team: str
    league: League

    odds: dict[Bookmaker, Odds1X2]
