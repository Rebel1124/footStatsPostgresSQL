from typing import Annotated

from pydantic import BeforeValidator, Field

from src.schemes.base import StrictBaseModel


@BeforeValidator
def remove_commas(num):
    if isinstance(num, str):
        return num.replace(",", "")
    return num


plain_float = Annotated[float, remove_commas]

type Results = dict[str, dict[str, plain_float]]

type OverUnder = dict[str, dict[str, plain_float]]


class YesNo(StrictBaseModel):
    Yes: dict[str, plain_float] = Field(default_factory=dict)
    No: dict[str, plain_float] = Field(default_factory=dict)


class OddsComparison(StrictBaseModel):
    ft_result: Results | None = Field(None, alias="FT Result")

    result_1_half: Results | None = Field(None, alias="Result 1st Half")
    corners_1x2: Results | None = Field(None, alias="Corners 1x2")
    result_2_half: OverUnder | None = Field(None, alias="Result 2nd Half")

    double_chance: Results | None = Field(None, alias="Double Chance")

    over_under: OverUnder | None = Field(None, alias="Over/Under")
    over_under_1_half: OverUnder | None = Field(None, alias="Over/Under 1st Half")
    over_under_2_half: OverUnder | None = Field(None, alias="Over/Under 2nd Half")
    corners_over_under: OverUnder | None = Field(None, alias="Corners Over Under")

    team_to_score_first: OverUnder | None = Field(None, alias="Team To Score First")

    clean_sheet_home: YesNo | None = Field(None, alias="Clean Sheet - Home")
    clean_sheet_away: YesNo | None = Field(None, alias="Clean Sheet - Away")

    both_teams_to_score: YesNo | None = Field(None, alias="Both Teams To Score")

    win_to_nil: Results | None = Field(None, alias="Win To Nil")

    btts_1_half: YesNo | None = Field(None, alias="BTTS 1st Half")
    btts_2_half: YesNo | None = Field(None, alias="BTTS 2nd Half")
