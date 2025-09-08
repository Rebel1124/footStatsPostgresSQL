from datetime import UTC, datetime
from typing import Literal
from urllib.parse import parse_qs, urlparse

import httpx
from pydantic import BaseModel

from src.config import BET_WAY_URLS, League

from . import MatchOdds


def get_bet_way_odds(client: httpx.Client, league: League) -> list[MatchOdds]:
    url = BET_WAY_URLS[league]
    parsed_params = parse_qs(urlparse(url).query)
    region, _league = parsed_params["selectedLeagues"][0].split("_")
    sort_order = parsed_params["sortOrder"]

    api_url = "https://new.betway.co.za/sportsapi/br/v1/BetBook/Filtered/"
    params = {
        "Take": 20,
        "Skip": 0,
        "isEsport": False,
        "sportID": "soccer",
        "countryCode": "ZA",
        "cultureCode": "en-US",
        "boostedOnly": False,
        "SortOrder": sort_order,
        "marketTypes": ["[Win/Draw/Win]"],
        "RegionAndLeagueIds[0].regionId": region,
        "RegionAndLeagueIds[0].leagueId": _league,
    }
    resp = client.get(api_url, params=params)
    resp.raise_for_status()
    data = BetWayResp.model_validate(resp.json())
    return list(parse_betway_odds(data))


class _Event(BaseModel):
    homeTeam: str
    awayTeam: str
    eventId: int
    expectedStartEpoch: int


class _Market(BaseModel):
    marketId: str
    eventId: int
    displayName: str | Literal["Booking 1X2", "1X2"]


class _Outcome(BaseModel):
    outcomeId: str
    displayName: str | Literal["Draw"]
    eventId: int
    marketId: str


class _Price(BaseModel):
    outcomeId: str
    priceDecimal: float


class BetWayResp(BaseModel):
    events: list[_Event]
    outcomes: list[_Outcome]
    markets: list[_Market]
    prices: list[_Price]


def parse_betway_odds(data: BetWayResp):
    events_markets = {
        m.eventId: m for m in data.markets if m.displayName in ("Booking 1X2", "1X2")
    }
    outcomes_prices = {p.outcomeId: p for p in data.prices}
    for event in data.events:
        market = events_markets[event.eventId]

        home_outcome_id, away_outcome_id, draw_outcome_id = (
            o.outcomeId for o in data.outcomes if o.marketId == market.marketId
        )

        game_time = datetime.fromtimestamp(event.expectedStartEpoch, UTC)

        yield MatchOdds(
            home_team=event.homeTeam,
            away_team=event.awayTeam,
            home_odds=outcomes_prices[home_outcome_id].priceDecimal,
            draw_odds=outcomes_prices[draw_outcome_id].priceDecimal,
            away_odds=outcomes_prices[away_outcome_id].priceDecimal,
            start_at=game_time,
        )
