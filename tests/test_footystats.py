import os
from datetime import datetime

import pytest
from dotenv import load_dotenv

from src.footystats import FootyStats, NotFound


@pytest.fixture
def footy_stats():
    load_dotenv()
    key = os.environ["FOOTYSTATS_API_KEY"]
    return FootyStats(key, 1)


def test_get_countries(footy_stats: FootyStats):
    countries = footy_stats.get_countries()
    assert countries


def test_get_leagues(footy_stats: FootyStats):
    leagues = footy_stats.get_leagues()
    assert leagues


def test_get_day_matches(footy_stats: FootyStats):
    day = datetime(2024, 7, 23)
    matches = footy_stats.get_day_matches(day)
    assert matches


def test_get_league_stats(footy_stats: FootyStats):
    stats = footy_stats.get_league_stats(2012)
    assert stats


def test_get_league_stats__not_found(footy_stats: FootyStats):
    with pytest.raises(NotFound):
        footy_stats.get_league_stats(20120)


def test_get_league_matches__not_found(footy_stats: FootyStats):
    with pytest.raises(NotFound):
        footy_stats.get_league_matches(20120)


def test_get_league_matches(footy_stats: FootyStats):
    matches = footy_stats.get_league_matches(2012)
    assert matches


def test_get_league_teams__not_found(footy_stats: FootyStats):
    with pytest.raises(NotFound):
        footy_stats.get_league_teams(20120)


def test_get_league_teams(footy_stats: FootyStats):
    teams = footy_stats.get_league_teams(2012)
    assert teams


def test_get_league_players__not_found(footy_stats: FootyStats):
    with pytest.raises(NotFound):
        footy_stats.get_league_players(20120)


def test_get_league_players(footy_stats: FootyStats):
    players = footy_stats.get_league_players(2012)
    assert len(players) > 600  # actually few pages


def test_get_league_referees__not_found(footy_stats: FootyStats):
    with pytest.raises(NotFound):
        footy_stats.get_league_referees(20120)


def test_get_league_referees(footy_stats: FootyStats):
    players = footy_stats.get_league_referees(2012)
    assert len(players) == 21


def test_get_team(footy_stats: FootyStats):
    team_states = footy_stats.get_team(60)
    assert len(team_states) > 45


def test_get_team__not_found(footy_stats: FootyStats):
    with pytest.raises(NotFound):
        footy_stats.get_team(201200)


def test_get_team_lastx(footy_stats: FootyStats):
    team_states = footy_stats.get_team_lastx(60)
    assert len(team_states) == 3  # last 5/6/10


def test_get_team_lastx__not_found(footy_stats: FootyStats):
    with pytest.raises(NotFound):
        footy_stats.get_team_lastx(201200)


def test_get_match_details__not_found(footy_stats: FootyStats):
    with pytest.raises(NotFound):
        footy_stats.get_match_details(20120)


def test_get_match_details(footy_stats: FootyStats):
    matches = footy_stats.get_match_details(578994)
    assert matches


def test_get_league_tables__not_found(footy_stats: FootyStats):
    with pytest.raises(NotFound):
        footy_stats.get_league_tables(2012389)


def test_get_league_tables(footy_stats: FootyStats):
    tables = footy_stats.get_league_tables(2012)
    assert tables


def test_get_btts_stats(footy_stats: FootyStats):
    stats = footy_stats.get_btts_stats()
    assert stats


def test_get_over25_stats(footy_stats: FootyStats):
    stats = footy_stats.get_over25_stats()
    assert stats
