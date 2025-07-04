from typing import Annotated, Literal

from pydantic import HttpUrl, StringConstraints

from .base import StrContinentCode, StrictBaseModel, validate_season_year


class LeaguePlayer(StrictBaseModel):
    id: int
    competition_id: int
    full_name: str
    first_name: str
    last_name: str
    known_as: str
    shorthand: str
    age: int
    height: int
    weight: int
    league: str
    league_type: str  # Literal["Domestic League", "Cup"]
    season: Annotated[str, validate_season_year]
    starting_year: int
    ending_year: int
    url: HttpUrl
    club_team_id: int
    club_team_2_id: int
    national_team_id: int
    position: Literal["Goalkeeper", "Defender", "Midfielder", "Forward", "Coach"]
    minutes_played_overall: int
    minutes_played_home: int
    minutes_played_away: int
    birthday: int
    nationality: Annotated[
        str,
        StringConstraints(strip_whitespace=True, to_lower=True),
    ]
    continent: StrContinentCode
    appearances_overall: int
    appearances_home: int
    appearances_away: int
    goals_overall: int
    goals_home: int
    goals_away: int
    clean_sheets_home: int
    clean_sheets_away: int
    clean_sheets_overall: int
    conceded_overall: int
    conceded_home: int
    conceded_away: int
    assists_overall: int
    assists_home: int
    assists_away: int
    penalty_goals: int
    penalty_misses: int
    penalty_success: int
    goals_involved_per_90_overall: float
    assists_per_90_overall: float
    goals_per_90_overall: float
    clean_sheets_per_overall: int
    goals_per_90_home: float
    goals_per_90_away: float
    min_per_goal_overall: int
    conceded_per_90_overall: float
    min_per_conceded_overall: int
    cards_overall: int
    yellow_cards_overall: int
    red_cards_overall: int
    min_per_match: int
    min_per_card_overall: int
    min_per_assist_overall: int
    cards_per_90_overall: float
    rank_in_league_top_attackers: int
    rank_in_league_top_midfielders: int
    rank_in_league_top_defenders: int
    rank_in_club_top_scorer: int
    last_match_timestamp: int
