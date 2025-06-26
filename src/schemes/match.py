from typing import Annotated, Literal

from pydantic import HttpUrl

from .base import (
    StrictBaseModel,
    add_base_domain,
    add_cdn_img_domain,
    validate_event_times,
    validate_season_year,
)


class Match(StrictBaseModel):
    id: int
    homeID: int
    awayID: int
    season: Annotated[str, validate_season_year]
    status: Literal["incomplete", "complete", "canceled", "suspended"]
    roundID: int
    game_week: int
    revised_game_week: Literal[-1]
    homeGoals: Annotated[list[str], validate_event_times]
    awayGoals: Annotated[list[str], validate_event_times]
    homeGoalCount: int
    awayGoalCount: int
    totalGoalCount: int
    team_a_corners: int
    team_b_corners: int
    totalCornerCount: int
    team_a_offsides: int
    team_b_offsides: int
    team_a_yellow_cards: int
    team_b_yellow_cards: int
    team_a_red_cards: int
    team_b_red_cards: int
    team_a_shotsOnTarget: int
    team_b_shotsOnTarget: int
    team_a_shotsOffTarget: int
    team_b_shotsOffTarget: int
    team_a_shots: int
    team_b_shots: int
    team_a_fouls: int
    team_b_fouls: int
    team_a_possession: int
    team_b_possession: int
    refereeID: int | None
    coach_a_ID: int | None
    coach_b_ID: int | None
    stadium_name: str
    stadium_location: str
    team_a_cards_num: int
    team_b_cards_num: int
    odds_ft_1: float
    odds_ft_x: float
    odds_ft_2: float
    HTGoalCount: int
    team_b_penalties_won: int
    o05_2H_potential: int
    odds_2nd_half_result_x: float
    team_b_cards_0_10_min: int
    team_a_penalty_goals: int
    u05_potential: int
    odds_ft_over15: float
    odds_btts_2nd_half_no: int
    o05HT_potential: int
    team_a_2h_corners: int
    odds_2nd_half_under25: float
    team_b_penalty_missed: int
    odds_corners_under_95: float
    odds_corners_over_115: float
    team_b_fh_corners: int
    odds_dnb_2: int
    corner_fh_count: int
    attacks_recorded: int
    team_a_xg: float
    team_a_throwins: int
    odds_corners_x: float
    total_xg_prematch: float
    cards_potential: float
    odds_1st_half_over15: float
    odds_btts_yes: float
    team_b_penalty_goals: int
    pre_match_teamA_overall_ppg: float
    odds_ft_over05: float
    freekicks_recorded: int
    avg_potential: float
    o15HT_potential: int
    matches_completed_minimum: int
    odds_corners_over_95: float
    odds_2nd_half_over35: float
    odds_corners_over_105: float
    odds_2nd_half_over25: float
    odds_corners_over_85: float
    GoalCount_2hg: int
    odds_doublechance_x2: float
    card_timings_recorded: int
    odds_2nd_half_over15: float
    odds_win_to_nil_2: float
    team_a_fh_corners: int
    odds_1st_half_result_2: float
    btts_2hg_potential: int
    pens_recorded: int
    odds_2nd_half_over05: float
    team_b_freekicks: int
    no_home_away: int
    goalTimingDisabled: int
    total_2h_cards: int
    odds_team_b_cs_yes: float
    odds_corners_2: float
    o15_potential: int
    team_b_0_10_min_goals: int
    odds_1st_half_over25: float
    homeGoals_timings: Annotated[list[str], validate_event_times]
    overallGoalCount: int
    u35_potential: int
    odds_doublechance_1x: float
    corner_timings_recorded: int
    team_b_dangerous_attacks: int
    corners_potential: float
    odds_team_to_score_first_1: float
    odds_team_b_cs_no: float
    ht_goals_team_a: int
    odds_ft_under15: float
    odds_team_a_cs_yes: float
    odds_2nd_half_under35: float
    odds_1st_half_over05: float
    match_url: Annotated[HttpUrl, add_base_domain]
    o35_potential: int
    team_a_freekicks: int
    team_a_attacks: int
    team_a_0_10_min_goals: int
    odds_ft_under45: float
    odds_corners_under_85: float
    btts_fhg_potential: int
    team_b_fh_cards: int
    o45_potential: int
    odds_ft_over25: float
    odds_btts_2nd_half_yes: int
    home_image: Annotated[HttpUrl, add_cdn_img_domain]
    home_name: str
    team_a_2h_cards: int
    away_url: Annotated[HttpUrl, add_base_domain]
    pre_match_away_ppg: float
    u45_potential: int
    throwins_recorded: int
    team_a_penalties_won: int
    corner_2h_count: int
    team_b_xg_prematch: float
    corners_o105_potential: int
    team_a_cards_0_10_min: int
    odds_team_to_score_first_x: float
    team_b_attacks: int
    odds_corners_over_75: float
    total_xg: float
    o05_potential: int
    awayGoals_timings: Annotated[list[str], validate_event_times]
    odds_ft_over45: float
    o15_2H_potential: int
    odds_ft_under05: float
    odds_btts_no: float
    odds_1st_half_under05: float
    team_b_throwins: int
    goals_2hg_team_b: int
    odds_dnb_1: int
    pre_match_home_ppg: float
    odds_ft_under25: float
    team_b_2h_cards: int
    team_a_corners_0_10_min: int
    home_ppg: float
    odds_team_to_score_first_2: float
    team_b_goalkicks: int
    odds_2nd_half_under15: float
    odds_ft_under35: float
    competition_id: int
    odds_doublechance_12: float
    odds_2nd_half_under05: float
    team_a_penalty_missed: int
    odds_1st_half_result_1: float
    odds_1st_half_under35: float
    team_b_xg: float
    team_a_dangerous_attacks: int
    team_a_fh_cards: int
    u15_potential: int
    corners_o85_potential: int
    odds_corners_under_115: float
    odds_btts_1st_half_yes: int
    odds_2nd_half_result_2: float
    odds_1st_half_under15: float
    odds_1st_half_result_x: float
    u25_potential: int
    odds_corners_under_105: float
    goal_timings_recorded: int
    odds_corners_under_75: float
    ht_goals_team_b: int
    attendance: int
    goals_2hg_team_a: int
    team_b_2h_corners: int
    away_image: Annotated[HttpUrl, add_cdn_img_domain]
    total_fh_cards: int
    odds_2nd_half_result_1: float
    odds_team_a_cs_no: float
    corners_o95_potential: int
    btts_potential: int
    team_b_corners_0_10_min: int
    away_name: str
    winningTeam: int
    odds_win_to_nil_1: float
    o25_potential: int
    odds_corners_1: float
    away_ppg: float
    odds_ft_over35: float
    odds_1st_half_under25: float
    team_a_xg_prematch: float
    pre_match_teamB_overall_ppg: float
    odds_1st_half_over35: float
    home_url: Annotated[HttpUrl, add_base_domain]
    goalkicks_recorded: int
    date_unix: int
    offsides_potential: float
    odds_btts_1st_half_no: int
    team_a_goalkicks: int
