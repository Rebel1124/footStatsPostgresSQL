from datetime import datetime
from typing import Literal
from urllib.parse import urlparse

import httpx
from pydantic import AliasPath, BaseModel, Field

from src.config import SPORTING_BET_URLS, League

from . import MatchOdds, get_http_client


def _get_sporting_bet_access_id(client: httpx.Client) -> str:
    resp = client.get(
        "https://www.sportingbet.co.za/en/api/clientconfig",
        headers={"x-bwin-sports-api": "prod"},
    )
    resp.raise_for_status()
    return ClientConfigResp.model_validate(resp.json()).msConnection.pushAccessId


class _Connection(BaseModel):
    pushAccessId: str


class ClientConfigResp(BaseModel):
    msConnection: _Connection


HEADERS = {
    "sec-ch-ua-platform": '"macOS"',
    "x-correlation-id": "598cf002a3b040bea1478c2fa1b8f945",
    "sec-ch-ua": '"Not=A?Brand";v="24", "Chromium";v="140"',
    "sec-ch-ua-mobile": "?0",
    "x-from-product": "host-app",
    "x-device-type": "desktop",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "accept": "application/json, text/plain, */*",
    "dnt": "1",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "accept-language": "en-US,en;q=0.9",
    "priority": "u=4, i",
}


def get_sporting_bet_odds(
    league: League,
) -> list[MatchOdds]:
    url = SPORTING_BET_URLS[league]
    competition_id = int(urlparse(url).path.removesuffix("/").split("-")[-1])
    with get_http_client() as client:
        access_id = _get_sporting_bet_access_id(client)
        resp = client.get(
            "https://www.sportingbet.co.za/cds-api/bettingoffer/fixtures",
            params={
                "userCountry": "ZA",
                "country": "ZA",
                "x-bwin-accessid": access_id,
                "lang": "en",
                "fixtureTypes": "Standard",
                "state": "Latest",
                "offerMapping": "MainMarkets",
                "sortBy": "FixtureStage",
                "competitionIds": competition_id,
                "skip": 0,
                "take": 50,
            },
            headers={
                **HEADERS,
                "x-bwin-browser-url": url,
                "referer": url,
            },
        )
    # open("resp.html", "w").write(resp.content.decode())
    resp.raise_for_status()
    data = SportingBetResp.model_validate(resp.json())
    return list(parse_sporting_bet_odds(data))


class _Option(BaseModel):
    name: str | Literal["Draw"] = Field(validation_alias=AliasPath("name", "value"))
    odds: float = Field(validation_alias=AliasPath("price", "odds"))


class _Market(BaseModel):
    name: str | Literal["Match Result", "Match Result - 2UP (EP)"] = Field(
        validation_alias=AliasPath("name", "value")
    )
    options: list[_Option]


class _Fixture(BaseModel):
    name: str | Literal["PairGame"] = Field(validation_alias=AliasPath("name", "value"))
    startDate: datetime
    optionMarkets: list[_Market]
    fixtureType: str


class SportingBetResp(BaseModel):
    fixtures: list[_Fixture]


def parse_sporting_bet_odds(data: SportingBetResp):
    for fixture in data.fixtures:
        if fixture.fixtureType != "PairGame":
            continue
        try:
            market = next(
                m for m in fixture.optionMarkets if m.name.startswith("Match Result")
            )
        except StopIteration:
            raise ValueError(
                f"Match Result market not found for fixture '{fixture.name}'"
            )
        home, draw, away = market.options
        yield MatchOdds(
            home_team=home.name,
            away_team=away.name,
            home_odds=home.odds,
            draw_odds=draw.odds,
            away_odds=away.odds,
            start_at=fixture.startDate,
        )
