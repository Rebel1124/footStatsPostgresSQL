import pytest

from src.config import League
from src.scrapers import Bookmaker, get_browser_context, get_http_client
from src.scrapers.all import aggregate_match_odds, get_league_matches_odds


@pytest.mark.parametrize("league", [League.ENGLAND_CHAMPIONSHIP])
def test_get_league_matches_odds_and_aggregate_them(league):
    res = get_league_matches_odds(league)

    assert set(res) == set(Bookmaker)
    aggregated_matches_odds = list(aggregate_match_odds(res, league))
    assert len(aggregated_matches_odds) == len(res[Bookmaker.BET_10])

    for odds in aggregated_matches_odds:
        assert set(odds.odds) == set(Bookmaker)
