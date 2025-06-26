from typing import Annotated

from .base import (
    StrictBaseModel,
    add_base_domain,
    empty_list_to_none,
)


class _Zone(StrictBaseModel):
    name: str | None
    number: int


class _SpecificTableItem(StrictBaseModel):
    id: int
    seasonGoals_home: int
    seasonConceded: int
    seasonGoals_away: int
    seasonConceded_away: int
    seasonConceded_home: int
    seasonGoals: int
    points: int
    points_original: int | None = None
    seasonGoalDifference: int
    seasonWins_home: int
    seasonWins_away: int
    seasonWins_overall: int
    seasonDraws_home: int
    seasonDraws_away: int
    seasonDraws_overall: int
    seasonLosses_away: int
    seasonLosses_home: int
    seasonLosses_overall: int
    matchesPlayed: int
    name: str
    country: str | None
    cleanName: str
    shortHand: str
    url: Annotated[str, add_base_domain]
    seasonURL_overall: Annotated[str, add_base_domain]
    seasonURL_home: Annotated[str, add_base_domain]
    seasonURL_away: Annotated[str, add_base_domain]
    position: int
    zone: Annotated[_Zone | None, empty_list_to_none]
    corrections: int
    wdl_record: str


class _AllMatchesTableOverAllItem(StrictBaseModel):
    id: int
    seasonGoals: int
    seasonConceded: int
    points: int
    seasonGoalDifference: int
    seasonLosses_away: int
    matchesPlayed: int
    name: str
    ppg_overall: float
    country: str
    cleanName: str
    shortHand: str
    url: Annotated[str, add_base_domain]
    seasonURL_overall: Annotated[str, add_base_domain]
    seasonURL_home: Annotated[str, add_base_domain]
    seasonURL_away: Annotated[str, add_base_domain]
    position: int
    corrections: int
    zone: Annotated[_Zone | None, empty_list_to_none]

    seasonGoalDifference: int
    seasonWins_home: int
    seasonWins_away: int
    seasonWins_overall: int
    seasonDraws_home: int
    seasonDraws_away: int
    seasonDraws_overall: int
    seasonLosses_away: int
    seasonLosses_home: int
    seasonLosses_overall: int
    seasonConceded_home: int
    seasonConceded_away: int
    seasonGoals_away: int
    seasonGoals_home: int


class _AllMatchesTableHomeItem(StrictBaseModel):
    seasonWins: int
    seasonDraws: int

    id: int
    seasonGoals: int
    seasonConceded: int
    points: int
    seasonGoalDifference: int
    matchesPlayed: int
    name: str
    country: str
    cleanName: str
    shortHand: str
    url: Annotated[str, add_base_domain]
    seasonURL_overall: Annotated[str, add_base_domain]
    seasonURL_home: Annotated[str, add_base_domain]
    seasonURL_away: Annotated[str, add_base_domain]
    position: int
    zone: Annotated[_Zone | None, empty_list_to_none]

    seasonLosses_away: int | None = None
    seasonLosses_home: int | None = None


class _AllMatchesTableAwayItem(_AllMatchesTableHomeItem):
    pass


class _LeagueTableItem(StrictBaseModel):
    id: int
    seasonGoals_home: int
    seasonConceded: int
    seasonGoals_away: int
    seasonConceded_away: int
    seasonConceded_home: int
    ppg_overall: float
    seasonGoals: int
    points: int
    seasonGoalDifference: int
    seasonWins_home: int
    seasonWins_away: int
    seasonWins_overall: int
    seasonDraws_home: int
    seasonDraws_away: int
    seasonDraws_overall: int
    seasonLosses_away: int
    seasonLosses_home: int
    seasonLosses_overall: int
    matchesPlayed: int
    name: str
    country: str | None
    cleanName: str
    shortHand: str
    url: Annotated[str, add_base_domain]
    seasonURL_overall: Annotated[str, add_base_domain]
    seasonURL_home: Annotated[str, add_base_domain]
    seasonURL_away: Annotated[str, add_base_domain]
    position: int
    zone: Annotated[_Zone | None, empty_list_to_none]
    corrections: int


class _Group(StrictBaseModel):
    name: str
    group_id: int
    table: list[_SpecificTableItem]


class _SpecificTable(StrictBaseModel):
    description: Annotated[str | None, empty_list_to_none]
    groups: list[_Group] | None
    round: str
    table: list[_SpecificTableItem] | None
    round_id: int


class LeagueTables(StrictBaseModel):
    league_table: list[_LeagueTableItem] | None
    all_matches_table_overall: list[_AllMatchesTableOverAllItem]
    all_matches_table_home: list[_AllMatchesTableHomeItem]
    all_matches_table_away: list[_AllMatchesTableAwayItem]
    specific_tables: list[_SpecificTable]
