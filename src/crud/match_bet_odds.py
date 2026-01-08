from typing import Any, Iterable

from sqlalchemy import insert
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import InstrumentedAttribute, Session

from src.db import MatchBetOddsDB
from src.models import AggregatedMatchOdds
from src.scrapers import Bookmaker


class NoneOdds1X2:
    home = None
    draw = None
    away = None


def upsert_matches_bet_odds(
    db: Session, matches: Iterable[AggregatedMatchOdds]
) -> None:
    values: list[dict[InstrumentedAttribute, Any]] = []
    for match in matches:

        def get_odds(b: Bookmaker):
            return match.odds.get(b, NoneOdds1X2)

        values.append(
            {
                MatchBetOddsDB.away_team: match.away_team,
                MatchBetOddsDB.home_team: match.home_team,
                MatchBetOddsDB.league_name: match.league.value,
                MatchBetOddsDB.date: match.start_at,
                MatchBetOddsDB.updated_at: match.actual_at,
                # ---
                MatchBetOddsDB.supersport_1: get_odds(Bookmaker.SUPER_SPORT_BET).home,
                MatchBetOddsDB.supersport_x: get_odds(Bookmaker.SUPER_SPORT_BET).draw,
                MatchBetOddsDB.supersport_2: get_odds(Bookmaker.SUPER_SPORT_BET).away,
                # ---
                MatchBetOddsDB.betway_1: get_odds(Bookmaker.BET_WAY).home,
                MatchBetOddsDB.betway_x: get_odds(Bookmaker.BET_WAY).draw,
                MatchBetOddsDB.betway_2: get_odds(Bookmaker.BET_WAY).away,
                # ---
                MatchBetOddsDB.hollywood_1: get_odds(Bookmaker.HOLLYWOOD_BETS).home,
                MatchBetOddsDB.hollywood_x: get_odds(Bookmaker.HOLLYWOOD_BETS).draw,
                MatchBetOddsDB.hollywood_2: get_odds(Bookmaker.HOLLYWOOD_BETS).away,
                # ---
                MatchBetOddsDB.bet10_1: get_odds(Bookmaker.BET_10).home,
                MatchBetOddsDB.bet10_x: get_odds(Bookmaker.BET_10).draw,
                MatchBetOddsDB.bet10_2: get_odds(Bookmaker.BET_10).away,
                # ---
                MatchBetOddsDB.sportingbet_1: get_odds(Bookmaker.SPORTING_BET).home,
                MatchBetOddsDB.sportingbet_x: get_odds(Bookmaker.SPORTING_BET).draw,
                MatchBetOddsDB.sportingbet_2: get_odds(Bookmaker.SPORTING_BET).away,
                # ---
                MatchBetOddsDB.supabets_1: get_odds(Bookmaker.SUPA_BETS).home,
                MatchBetOddsDB.supabets_x: get_odds(Bookmaker.SUPA_BETS).draw,
                MatchBetOddsDB.supabets_2: get_odds(Bookmaker.SUPA_BETS).away,
                # ---
                MatchBetOddsDB.pinnacle_1: get_odds(Bookmaker.PINNACLE).home,
                MatchBetOddsDB.pinnacle_x: get_odds(Bookmaker.PINNACLE).draw,
                MatchBetOddsDB.pinnacle_2: get_odds(Bookmaker.PINNACLE).away,
            }
        )

    if not values:
        raise ValueError("No matches passed")

    stmt = insert(MatchBetOddsDB).values(values)
    update_set = {
        col: getattr(stmt.excluded, col.key)
        for col in values[0]
        if col
        not in (MatchBetOddsDB.date, MatchBetOddsDB.home_team, MatchBetOddsDB.away_team)
    }
    stmt = stmt.on_conflict_do_update(
        index_elements=(MatchBetOddsDB.home_team, MatchBetOddsDB.date), set_=update_set
    )

    db.execute(stmt)
