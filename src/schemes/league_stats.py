from typing import Annotated, Literal

from pydantic import BaseModel, HttpUrl

from .base import (
    StrContinentCode,
    StrictBaseModel,
    validate_event_times,
    validate_season_year,
)


class _LeaguePlayer(BaseModel):
    id: int


class LeagueStats(StrictBaseModel):
    id: int
    name: str
    english_name: str
    shortHand: str
    status: Literal["Incompleted", "Completed", "In Progress"]

    # Name
    name_jp: str | None
    name_tr: str | None
    name_kr: str | None
    name_pt: str | None
    name_ru: str | None
    name_es: str | None
    name_se: str | None
    name_de: str | None
    name_zht: str | None
    name_nl: str | None
    name_it: str | None
    name_fr: str | None
    name_id: str | None
    name_pl: str | None
    name_gr: str | None
    name_dk: str | None
    name_th: str | None
    name_hr: str | None
    name_ro: str | None
    name_in: str | None
    name_no: str | None
    name_hu: str | None
    name_cz: str | None
    name_cn: str | None
    name_ara: str | None
    name_si: str | None
    name_vn: str | None
    name_my: str | None
    name_sk: str | None
    name_rs: str | None
    name_ua: str | None
    name_bg: str | None
    name_lv: str | None
    name_ge: str | None
    name_swa: str | None
    name_kur: str | None
    name_ee: str | None
    name_lt: str | None
    name_ba: str | None
    name_by: str | None
    name_fi: str | None

    country: str
    domestic_scale: int
    international_scale: int
    format: str
    division: int
    no_home_away: int | None
    starting_year: int
    ending_year: int
    women: bool
    continent: StrContinentCode
    comp_master_id: int
    image: HttpUrl
    clubNum: int
    season: Annotated[str, validate_season_year]  # 2019/2020
    goalTimingDisabled: int
    totalMatches: int
    matchesCompleted: int
    canceledMatchesNum: int
    game_week: int
    total_game_week: int
    round: int
    progress: int
    total_goals: int
    home_teams_goals: int
    home_teams_conceded: int
    away_teams_goals: int
    away_teams_conceded: int
    seasonAVG_overall: float
    seasonAVG_home: float
    seasonAVG_away: float
    btts_matches: int
    seasonBTTSPercentage: int
    seasonCSPercentage: int
    home_teams_clean_sheets: int
    away_teams_clean_sheets: int
    home_teams_failed_to_score: int
    away_teams_failed_to_score: int
    riskNum: int
    homeAttackAdvantagePercentage: int
    homeDefenceAdvantagePercentage: int
    homeOverallAdvantage: int
    cornersAVG_overall: float
    cornersAVG_home: float
    cornersAVG_away: float
    cornersTotal_overall: int
    cornersTotal_home: int
    cornersTotal_away: int
    cardsAVG_overall: float
    cardsAVG_home: float
    cardsAVG_away: float
    cardsTotal_overall: int
    cardsTotal_home: int
    cardsTotal_away: int
    foulsTotal_overall: int
    foulsTotal_home: int
    foulsTotal_away: int
    foulsAVG_overall: float
    foulsAVG_home: float
    foulsAVG_away: float
    shotsTotal_overall: int
    shotsTotal_home: int
    shotsTotal_away: int
    shotsAVG_overall: float
    shotsAVG_home: float
    shotsAVG_away: float
    offsidesTotal_overall: int
    offsidesTotal_home: int
    offsidesTotal_away: int
    offsidesAVG_overall: float
    offsidesAVG_home: float
    offsidesAVG_away: float
    offsidesOver05_overall: int
    offsidesOver15_overall: int
    offsidesOver25_overall: int
    offsidesOver35_overall: int
    offsidesOver45_overall: int
    offsidesOver55_overall: int
    offsidesOver65_overall: int
    over05OffsidesPercentage_overall: int
    over15OffsidesPercentage_overall: int
    over25OffsidesPercentage_overall: int
    over35OffsidesPercentage_overall: int
    over45OffsidesPercentage_overall: int
    over55OffsidesPercentage_overall: int
    over65OffsidesPercentage_overall: int
    seasonOver05Percentage_overall: int
    seasonOver15Percentage_overall: int
    seasonOver25Percentage_overall: int
    seasonOver35Percentage_overall: int
    seasonOver45Percentage_overall: int
    seasonOver55Percentage_overall: int
    seasonUnder05Percentage_overall: int
    seasonUnder15Percentage_overall: int
    seasonUnder25Percentage_overall: int
    seasonUnder35Percentage_overall: int
    seasonUnder45Percentage_overall: int
    seasonUnder55Percentage_overall: int
    cornersRecorded_matches: int
    cardsRecorded_matches: int
    offsidesRecorded_matches: int
    over65Corners_overall: int
    over75Corners_overall: int
    over85Corners_overall: int
    over95Corners_overall: int
    over105Corners_overall: int
    over115Corners_overall: int
    over125Corners_overall: int
    over135Corners_overall: int
    over145Corners_overall: int
    over65CornersPercentage_overall: int
    over75CornersPercentage_overall: int
    over85CornersPercentage_overall: int
    over95CornersPercentage_overall: int
    over105CornersPercentage_overall: int
    over115CornersPercentage_overall: int
    over125CornersPercentage_overall: int
    over135CornersPercentage_overall: int
    over145CornersPercentage_overall: int
    over05Cards_overall: int
    over15Cards_overall: int
    over25Cards_overall: int
    over35Cards_overall: int
    over45Cards_overall: int
    over55Cards_overall: int
    over65Cards_overall: int
    over75Cards_overall: int
    over05CardsPercentage_overall: int
    over15CardsPercentage_overall: int
    over25CardsPercentage_overall: int
    over35CardsPercentage_overall: int
    over45CardsPercentage_overall: int
    over55CardsPercentage_overall: int
    over65CardsPercentage_overall: int
    over75CardsPercentage_overall: int
    homeWins: int
    draws: int
    awayWins: int
    homeWinPercentage: int
    drawPercentage: int
    awayWinPercentage: int
    shotsRecorded_matches: int
    foulsRecorded_matches: int
    failed_to_score_total: int
    clean_sheets_total: int
    round_format: int
    goals_min_0_to_10: int
    goals_min_11_to_20: int
    goals_min_21_to_30: int
    goals_min_31_to_40: int
    goals_min_41_to_50: int
    goals_min_51_to_60: int
    goals_min_61_to_70: int
    goals_min_71_to_80: int
    goals_min_81_to_90: int
    goals_min_0_to_15: int
    goals_min_16_to_30: int
    goals_min_31_to_45: int
    goals_min_46_to_60: int
    goals_min_61_to_75: int
    goals_min_76_to_90: int
    player_count: int
    over05_fhg_num: int
    over15_fhg_num: int
    over25_fhg_num: int
    over35_fhg_num: int
    over05_fhg_percentage: int
    over15_fhg_percentage: int
    over25_fhg_percentage: int
    over35_fhg_percentage: int
    over05_2hg_num: int
    over15_2hg_num: int
    over25_2hg_num: int
    over35_2hg_num: int
    over05_2hg_percentage: int
    over15_2hg_percentage: int
    over25_2hg_percentage: int
    over35_2hg_percentage: int
    goalTimingsRecorded_num: int
    averageAttendance: int
    cornerTimingRecorded_matches: int
    corners_fh_num: int
    corners_2h_num: int
    corners_fh_avg: float
    corners_2h_avg: float
    corners_fh_over4_num: int
    corners_2h_over4_num: int
    corners_fh_over4_percentage: int
    corners_2h_over4_percentage: int
    corners_fh_over5_num: int
    corners_2h_over5_num: int
    corners_fh_over5_percentage: int
    corners_2h_over5_percentage: int
    corners_fh_over6_num: int
    corners_2h_over6_num: int
    corners_fh_over6_percentage: int
    corners_2h_over6_percentage: int
    attack_num_recoded_matches: int
    dangerous_attacks_num: int
    attacks_num: int
    dangerous_attacks_avg: float
    attacks_avg: float
    xg_avg: float
    possessions_recorded_matches: int
    seasonOver05_num: int
    seasonOver15_num: int
    seasonOver25_num: int
    seasonOver35_num: int
    seasonOver45_num: int
    seasonOver55_num: int
    seasonUnder05_num: int
    seasonUnder15_num: int
    seasonUnder25_num: int
    seasonUnder35_num: int
    seasonUnder45_num: int
    seasonUnder55_num: int
    db_english_name: str
    iso: str
    type: str
    footystats_url: HttpUrl

    seasonGoalsScored_home_teams: Annotated[list[str], validate_event_times]
    seasonGoalsScored_away_teams: Annotated[list[str], validate_event_times]
    seasonConceded_away_teams: Annotated[list[str], validate_event_times]
    seasonConceded_home_teams: Annotated[list[str], validate_event_times]

    top_scorers: list[_LeaguePlayer]
    top_assists: list[_LeaguePlayer]
    top_clean_sheets: list[_LeaguePlayer]
