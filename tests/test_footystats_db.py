from src.config import FOOTYSTATS_API_KEY
from src.footystats import FootyStats
from src.footystats_db import (
    add_match_details_to_db,
    get_match_details_from_db,
    get_missing_match_ids,
    get_missing_team_ids,
    get_season_from_db,
    get_stats_from_db,
    get_team_from_db,
    upsert_season_to_db,
    upsert_stats_in_db,
    upsert_team_to_db,
)
from src.schemes.season import SeasonMetaData
from src.utils import fetch_season


def test_add_and_get_season():
    footy = FootyStats(FOOTYSTATS_API_KEY, 2)
    season = fetch_season(
        footy, SeasonMetaData(season_id=25, season_year="2025", league_name="TEST")
    )
    upsert_season_to_db(season)
    season_db = get_season_from_db(season.season_id)
    assert season_db

    assert season_db.model_dump(exclude={"updated_at"}) == season.model_dump()
    assert season_db.season_id == 25
    assert season_db.season_year == "2025"
    assert season_db.league_name == "TEST"


def test_add_and_get_stats():
    footy = FootyStats(FOOTYSTATS_API_KEY, 2)
    btts = footy.get_btts_stats()
    over25 = footy.get_over25_stats()

    upsert_stats_in_db(btts, over25)
    old_stats = get_stats_from_db()
    upsert_stats_in_db(btts, over25)
    stats = get_stats_from_db()

    assert stats.updated_at > old_stats.updated_at
    assert stats.btts_stats.model_dump() == btts.model_dump()
    assert stats.over25_stats.model_dump() == over25.model_dump()


def test_add_and_get_match_details():
    footy = FootyStats(FOOTYSTATS_API_KEY, 2)
    match_details = footy.get_match_details(579101)

    add_match_details_to_db(match_details)
    details = get_match_details_from_db(match_details.id)

    assert details
    assert match_details.model_dump() == details.match_details.model_dump()


def test_get_missing_match_ids():
    footy = FootyStats(FOOTYSTATS_API_KEY, 2)
    details = footy.get_match_details(579190)
    add_match_details_to_db(details)

    ids = get_missing_match_ids({1, 2, 3, 579190})
    assert ids == {1, 2, 3}


def test_get_missing_team_ids():
    footy = FootyStats(FOOTYSTATS_API_KEY, 2)
    snapshots = footy.get_team(59)
    upsert_team_to_db(snapshots)

    ids = get_missing_team_ids({1, 2, 3, 59})
    assert ids == {1, 2, 3}


def test_add_and_get_team():
    footy = FootyStats(FOOTYSTATS_API_KEY, 2)
    team = footy.get_team(590)
    team_last_x = footy.get_team_lastx(590)

    upsert_team_to_db(team)
    old_team_last = get_team_from_db(590)
    upsert_team_to_db(team, team_last_x)
    team_db = get_team_from_db(590)

    assert team_db and old_team_last
    assert team_db.update_at > old_team_last.update_at
    assert [snapshot.model_dump() for snapshot in team] == [
        snapshot.model_dump() for snapshot in team_db.team_snapshots
    ]
    assert [snapshot.model_dump() for snapshot in team] == [
        snapshot.model_dump() for snapshot in team_db.team_snapshots
    ]
