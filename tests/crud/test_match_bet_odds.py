import random
from datetime import UTC, datetime

import pytest
from sqlalchemy import sql
from sqlalchemy.orm import Session

from src.config import League
from src.crud.match_bet_odds import upsert_matches_bet_odds
from src.db import MatchBetOddsDB
from src.models import AggregatedMatchOdds, Odds1X2
from src.scrapers import Bookmaker


def get_random_dt():
    return datetime.fromtimestamp(random.randint(1, 100000), UTC)


def get_random_odds1X2():
    return Odds1X2(
        home=random.random(),
        draw=random.random(),
        away=random.random(),
    )


def get_random_odds():
    return {b: get_random_odds1X2() for b in Bookmaker}


def get_random_match(
    home_team: str | None = None,
    away_team: str | None = None,
    start_at: datetime | None = None,
):
    return AggregatedMatchOdds(
        home_team=home_team or str(random.random()),
        away_team=away_team or str(random.random()),
        actual_at=get_random_dt(),
        start_at=start_at or get_random_dt(),
        odds=get_random_odds(),
        league=random.choice(list(League)),
    )


def assert_match(match: AggregatedMatchOdds, match_db: MatchBetOddsDB):
    assert match.home_team == match_db.home_team
    assert match.away_team == match_db.away_team
    assert match.league.value == match_db.league_name

    assert match.start_at == match_db.date
    assert match.actual_at == match_db.updated_at

    assert match.odds[Bookmaker.SUPER_SPORT_BET].draw == match_db.supersport_x
    assert match.odds[Bookmaker.SUPER_SPORT_BET].away == match_db.supersport_2
    assert match.odds[Bookmaker.SUPER_SPORT_BET].home == match_db.supersport_1

    assert match.odds[Bookmaker.BET_WAY].draw == match_db.betway_x
    assert match.odds[Bookmaker.BET_WAY].away == match_db.betway_2
    assert match.odds[Bookmaker.BET_WAY].home == match_db.betway_1

    assert match.odds[Bookmaker.HOLLYWOOD_BETS].draw == match_db.hollywood_x
    assert match.odds[Bookmaker.HOLLYWOOD_BETS].away == match_db.hollywood_2
    assert match.odds[Bookmaker.HOLLYWOOD_BETS].home == match_db.hollywood_1

    assert match.odds[Bookmaker.BET_10].draw == match_db.bet10_x
    assert match.odds[Bookmaker.BET_10].away == match_db.bet10_2
    assert match.odds[Bookmaker.BET_10].home == match_db.bet10_1

    assert match.odds[Bookmaker.SPORTING_BET].draw == match_db.sportingbet_x
    assert match.odds[Bookmaker.SPORTING_BET].away == match_db.sportingbet_2
    assert match.odds[Bookmaker.SPORTING_BET].home == match_db.sportingbet_1

    assert match.odds[Bookmaker.SUPA_BETS].draw == match_db.supabets_x
    assert match.odds[Bookmaker.SUPA_BETS].away == match_db.supabets_2
    assert match.odds[Bookmaker.SUPA_BETS].home == match_db.supabets_1


def test_upsert_match_bet_odds__insert(db: Session):
    matches = [get_random_match(), get_random_match()]
    matches.sort(key=lambda m: m.home_team)

    upsert_matches_bet_odds(db, matches)

    matches_db = sorted(
        db.scalars(sql.select(MatchBetOddsDB)), key=lambda m: m.home_team
    )
    for m, m_db in zip(matches, matches_db):
        assert_match(m, m_db)


def test_upsert_match_bet_odds__insert_and_update(db: Session):
    match = get_random_match()
    upsert_matches_bet_odds(db, [match])
    matches = [
        get_random_match(match.home_team, match.away_team, match.start_at),
        get_random_match(),
    ]

    upsert_matches_bet_odds(db, matches)

    matches_db = sorted(
        db.scalars(sql.select(MatchBetOddsDB)), key=lambda m: m.home_team
    )

    all_matches = sorted(matches, key=lambda m: m.home_team)
    for m, m_db in zip(all_matches, matches_db):
        assert_match(m, m_db)


def test_upsert_match_bet_odds__no_values(db: Session):
    with pytest.raises(ValueError):
        upsert_matches_bet_odds(db, [])
