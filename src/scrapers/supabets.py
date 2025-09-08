import re
from datetime import UTC, datetime, timedelta

import httpx
from pydantic import AliasPath, BaseModel, Field, field_validator

from src.config import SUPA_BETS_LEAGUE_IDS, League
from src.utils import datetime_to_ticks

from . import MatchOdds


def get_supa_bets_odds(client: httpx.Client, league: League) -> list[MatchOdds]:
    league_id = SUPA_BETS_LEAGUE_IDS[league]
    today = datetime.today().replace(tzinfo=UTC)
    resp = client.post(
        "https://www.supabets.co.za/Controls/ControlsWS.asmx/OddsViewFullEvent",
        json={
            "IDEvento": league_id,
            "IDGruppoQuota": -1,
            "IsGoalscorer": False,
            "TipoVisualizzazione": 1,
            "DataInizio": datetime_to_ticks(today),
            "DataFine": datetime_to_ticks(today + timedelta(days=7)),
        },
    )
    resp.raise_for_status()
    data = SupabetsData.model_validate(resp.json())
    return list(parse_supa_bets_odds(data))


class _Event(BaseModel):
    name: str = Field(validation_alias="SottoEvento")
    home_odds: float = Field(validation_alias=AliasPath("Quote", 0, "QuotaValore"))
    draw_odds: float = Field(validation_alias=AliasPath("Quote", 1, "QuotaValore"))
    away_odds: float = Field(validation_alias=AliasPath("Quote", 2, "QuotaValore"))
    time: datetime = Field(validation_alias="DataInizio")

    @field_validator("time", mode="before")
    def time_validator(time):
        if isinstance(time, str):
            if timestamp := re.search(r"\d+", time):
                return datetime.fromtimestamp(int(timestamp.group()) / 1000, UTC)
        return time


class SupabetsData(BaseModel):
    events: list[_Event] = Field(
        validation_alias=AliasPath("d", "Detail", "SottoEventiList")
    )


def parse_supa_bets_odds(data: SupabetsData):
    for event in data.events:
        home_team, away_team = event.name.split(" - ")
        yield MatchOdds(
            home_team=home_team,
            away_team=away_team,
            home_odds=event.home_odds,
            draw_odds=event.draw_odds,
            away_odds=event.away_odds,
            start_at=event.time,
        )
