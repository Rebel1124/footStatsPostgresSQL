from typing import Annotated, Literal

from src.schemes.base import StrictBaseModel
from src.schemes.odds_comparison import OddsComparison

from .base import empty_list_to_none, minus_one_to_none, validate_event_time
from .match import Match
from .weather import Weather

EventTime = Annotated[str, validate_event_time]


class _GoalDetails(StrictBaseModel):
    player_id: int
    assist_player_id: int
    time: str
    extra: Annotated[str | None, minus_one_to_none]
    goal_smid: int | None = None
    type: None | str = None


class _CardDetails(StrictBaseModel):
    player_id: int
    card_type: Literal["Yellow", "Second Yellow", "Red"]
    time: EventTime


class _PlayerEvent(StrictBaseModel):
    event_type: (
        str
        | Literal[
            "Yellow",
            "Goal",
            "Own Goal",
            "Penalty Goal",
            "Second Yellow",
            "Red",
            "Penalty Miss",
        ]
    )
    event_time: EventTime


class _LineupsPlayer(StrictBaseModel):
    player_id: int
    shirt_number: int
    player_events: list[_PlayerEvent]


class _BenchPlayer(StrictBaseModel):
    player_in_id: int
    player_out_id: int
    player_in_shirt_number: int
    player_out_time: EventTime
    player_in_events: list[_PlayerEvent]


class _Lineups(StrictBaseModel):
    team_a: list[_LineupsPlayer]
    team_b: list[_LineupsPlayer]


class _Bench(StrictBaseModel):
    team_a: list[_BenchPlayer]
    team_b: list[_BenchPlayer]


class _PreviousMatchesResults(StrictBaseModel):
    team_a_win_home: int
    team_a_win_away: int
    team_b_win_home: int
    team_b_win_away: int
    draw: int
    team_a_wins: int
    team_b_wins: int
    totalMatches: int
    team_a_win_percent: int
    team_b_win_percent: int


class _BettingStats(StrictBaseModel):
    over05: int
    over15: int
    over25: int
    over35: int
    over45: int
    over55: int
    btts: int
    clubACS: int
    clubBCS: int
    over05Percentage: int
    over15Percentage: int
    over25Percentage: int
    over35Percentage: int
    over45Percentage: int
    over55Percentage: int
    bttsPercentage: int
    clubACSPercentage: int
    clubBCSPercentage: int
    avg_goals: float
    total_goals: int


class _PreviousMatchesIds(StrictBaseModel):
    id: int
    date_unix: int
    team_a_id: int
    team_b_id: int
    team_a_goals: int
    team_b_goals: int


class _H2H(StrictBaseModel):
    team_a_id: int
    team_b_id: int
    previous_matches_results: _PreviousMatchesResults
    betting_stats: _BettingStats
    previous_matches_ids: list[_PreviousMatchesIds]


class _Trends(StrictBaseModel):
    home: list[tuple[Literal["great", "bad", "chart"], str]]
    away: list[tuple[Literal["great", "bad", "chart"], str]]


class MatchDetails(Match):
    lineups: _Lineups
    bench: _Bench
    team_a_goal_details: list[_GoalDetails]
    team_b_goal_details: list[_GoalDetails]
    trends: None | _Trends
    team_a_card_details: list[_CardDetails]
    team_b_card_details: list[_CardDetails]
    h2h: _H2H
    gpt_en: None | str
    gpt_int: None | dict[str, str]
    tv_stations: list[str] | None = None
    weather: Weather | None = None
    odds_comparison: Annotated[OddsComparison | None, empty_list_to_none] = None
