from datetime import datetime
from typing import Literal
from urllib.parse import urlparse

from pydantic import BaseModel

from src.config import HOOLYWOOD_BET_URLS, League

from . import MatchOdds, get_http_client


def get_hollywood_bets_odds(league: League) -> list[MatchOdds]:
    url = HOOLYWOOD_BET_URLS[league]
    parts = [p for p in urlparse(url).path.split("/") if p != ""]

    # betting/1/soccer/all/2/south-africa/3092935/sa-mfc
    _, sport_id, _, _, category_id, _, tournament_id, _ = parts

    url = f"https://sport-events-api.hollywoodbets.net/api/events/eps/sports/{sport_id}/categories/{category_id}/tournaments/{tournament_id}/events?withBetTypeId=15"
    with get_http_client() as client:
        resp = client.get(url)
    resp.raise_for_status()
    data = SportEventsResp.model_validate(resp.json())
    return list(parse_hollywodd_bets_odds(data))


class _Market(BaseModel):
    odds: float | None
    name: str | Literal["DRAW"]


class _BetType(BaseModel):
    markets: list[_Market]


class _Event(BaseModel):
    startTime: datetime
    betTypes: list[_BetType]
    name: str


class SportEventsResp(BaseModel):
    events: list[_Event]


def parse_hollywodd_bets_odds(data: SportEventsResp):
    for event in data.events:
        if " vs " not in event.name:
            continue

        bets = event.betTypes
        if len(bets) == 0:
            home_team, away_team = event.name.split(" vs ")
            home = _Market(odds=None, name=home_team)
            draw = _Market(odds=None, name="DRAW")
            away = _Market(odds=None, name=away_team)
        else:
            home, draw, away = bets[0].markets

        yield MatchOdds(
            home_team=home.name,
            away_team=away.name,
            home_odds=home.odds,
            draw_odds=draw.odds,
            away_odds=away.odds,
            start_at=event.startTime,
        )
