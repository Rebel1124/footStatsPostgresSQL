from datetime import datetime
from typing import Literal
from urllib.parse import urlparse

import httpx
from pydantic import AliasPath, BaseModel, Field

from src.config import SPORTING_BET_URLS, League

from . import MatchOdds


def get_sporting_bet_access_id(client: httpx.Client) -> str:
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


def get_sporting_bet_odds(
    client: httpx.Client, league: League, *, access_id: str
) -> list[MatchOdds]:
    url = SPORTING_BET_URLS[league]
    competition_id = int(urlparse(url).path.removesuffix("/").split("-")[-1])
    resp = client.get(
        "https://www.sportingbet.co.za/cds-api/bettingoffer/fixtures",
        params={
            "userCountry": "HR",
            "country": "HR",
            "x-bwin-accessid": access_id,
            "lang": "en",
            "fixtureTypes": "Standard",
            "state": "Latest",
            "offerMapping": "MainMarkets",
            "sortBy": "FixtureStage",
            "competitionIds": competition_id,
        },
    )
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
