from datetime import datetime
from typing import Literal

import httpx
from pydantic import BaseModel

from src.config import BET_10_LEAGUE_IDS, League

from . import MatchOdds, get_http_client


def get_bet_10_odds(league: League) -> list[MatchOdds]:
    league_id = BET_10_LEAGUE_IDS[league]
    content_temp = r'{"operationName":"listEvents","variables":{"payload":{"leagueId":"%s","eventType":"ALL"}},"query":"query listEvents($payload: ListEventsRequest!) {\n  listEvents(payload: $payload) {\n    events {\n      id\n      name\n      leagueId\n      leagueName\n      regionName\n      regionId\n      sportId\n      sportName\n      isLive\n      startEventDate\n      participantHomeName\n      participantAwayName\n      totalHomeScore\n      totalAwayScore\n      earlyPayoutId\n      markets {\n        id\n        name\n        marketLines {\n          id\n          name\n          isSuspended\n          marketLineStatus\n          selections {\n            id\n            name\n            odds\n            isActive\n            pillar\n            __typename\n          }\n          isMidline\n          __typename\n        }\n        numberOfColumns\n        marketFamilyIds\n        combinedId\n        isPillarSelectionSorting\n        marketStatus\n        __typename\n      }\n      totalMarketsCount\n      isSuspended\n      scoreboardEventId\n      eventPhase {\n        showPhase\n        description\n        __typename\n      }\n      urlPath\n      eventFamily\n      producerFamily\n      eventStatus\n      homeDismissals\n      awayDismissals\n      over\n      home {\n        name\n        id\n        isBatting\n        __typename\n      }\n      away {\n        name\n        id\n        isBatting\n        __typename\n      }\n      __typename\n    }\n    earlyPayoutPromotion {\n      id\n      highScoring\n      lowScoring\n      marketIds\n      termsAndConditions\n      supportOnLive {\n        overs\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"}'
    with get_http_client() as client:
        resp = client.post(
            "https://www.10bet.co.za/graphql",
            content=content_temp % league_id,
            headers={"content-type": "application/json", "accept": "application/json"},
        )
    resp.raise_for_status()
    data = Bet10Resp.model_validate(resp.json())
    return list(parse_10bet_odds(data))


class _Selection(BaseModel):
    name: str
    odds: float


class _MarketLine(BaseModel):
    selections: list[_Selection]


class _Market(BaseModel):
    name: str | Literal["1x2"]
    marketLines: list[_MarketLine]


class _Event(BaseModel):
    name: str
    markets: list[_Market]

    startEventDate: datetime


class _ListEvents(BaseModel):
    events: list[_Event]


class _Data(BaseModel):
    listEvents: _ListEvents


class Bet10Resp(BaseModel):
    data: _Data


def parse_10bet_odds(data: Bet10Resp):
    for event in data.data.listEvents.events:
        try:
            market = next(m for m in event.markets if m.name == "1x2")
        except StopIteration:
            raise Exception(f"Not found 1x2 market for event.name={event.name}")
        [market_line] = market.marketLines
        home, draw, away = market_line.selections

        yield MatchOdds(
            home_team=home.name,
            away_team=away.name,
            home_odds=home.odds,
            draw_odds=draw.odds,
            away_odds=away.odds,
            start_at=event.startEventDate,
        )
