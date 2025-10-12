import difflib
from collections import defaultdict
from collections.abc import Iterable
from datetime import UTC, datetime
from typing import assert_never

from loguru import logger
from playwright import sync_api as playwright
from pydantic import ValidationError

from src.config import (
    League,
)
from src.models import AggregatedMatchOdds, Odds1X2
from src.scrapers import Bookmaker, MatchOdds, get_browser_context
from src.scrapers.bet10 import get_bet_10_odds
from src.scrapers.betway import get_bet_way_odds
from src.scrapers.hollywood import get_hollywood_bets_odds
from src.scrapers.pinnacle import get_pinnacle_odds
from src.scrapers.sportingbet import get_sporting_bet_odds
from src.scrapers.supabets import get_supa_bets_odds
from src.scrapers.supersport import get_super_sport_bet_odds


def aggregate_match_odds(odds: dict[Bookmaker, list[MatchOdds]], league: League):
    map: defaultdict[datetime, defaultdict[Bookmaker, list[MatchOdds]]] = defaultdict(
        lambda: defaultdict(list)
    )
    now = datetime.now(UTC)
    for bookmaker, matches in odds.items():
        for match in matches:
            if now <= match.start_at:
                map[match.start_at][bookmaker].append(match)

    for match in odds[Bookmaker.BET_10]:
        match_odds = AggregatedMatchOdds(
            actual_at=now,
            home_team=match.home_team,
            away_team=match.away_team,
            start_at=match.start_at,
            league=league,
            odds={
                Bookmaker.BET_10: Odds1X2(
                    home=match.home_odds, draw=match.draw_odds, away=match.draw_odds
                )
            },
        )

        for bookmaker, matches in map[match.start_at].items():
            similar_match = _get_most_similar_match(match, matches)
            if similar_match is None:
                logger.warning(
                    f"No similar match found for {match!r}\n in {bookmaker} {league}\n in {matches}"
                )
                continue
            matches.remove(similar_match)  # optimization

            match_odds.odds[bookmaker] = Odds1X2(
                home=similar_match.home_odds,
                draw=similar_match.draw_odds,
                away=similar_match.draw_odds,
            )

        yield match_odds


def get_bet_odds(
    bookmaker: Bookmaker, league: League, page: playwright.Page, *, retries: int
) -> list[MatchOdds]:
    try:
        match bookmaker:
            case Bookmaker.SUPER_SPORT_BET:
                return get_super_sport_bet_odds(page, league)
            case Bookmaker.BET_WAY:
                return get_bet_way_odds(league)
            case Bookmaker.HOLLYWOOD_BETS:
                return get_hollywood_bets_odds(league)
            case Bookmaker.BET_10:
                return get_bet_10_odds(league)
            case Bookmaker.SPORTING_BET:
                return get_sporting_bet_odds(league)
            case Bookmaker.SUPA_BETS:
                return get_supa_bets_odds(league)
            case Bookmaker.PINNACLE:
                return get_pinnacle_odds(page, league)
            case _:
                assert_never(bookmaker)
    except Exception as e:
        if isinstance(e, ValidationError):
            raise e

        if retries == 0:
            logger.opt(exception=e).warning(
                "Failed to get bet odds for {} {}", bookmaker, league
            )

            raise e

        logger.debug(
            "Failed to get bet odds for {} {} | retries left {}",
            bookmaker,
            league,
            retries,
        )
        return get_bet_odds(bookmaker, league, page, retries=retries - 1)


def get_league_matches_odds(
    league: League,
    bookmakers: Iterable[Bookmaker] = Bookmaker,
):
    res: dict[Bookmaker, list[MatchOdds]] = {}

    with get_browser_context() as context:
        page = context.new_page()
        for bookmaker in bookmakers:
            res[bookmaker] = get_bet_odds(bookmaker, league, page, retries=3)

    return res


def _get_most_similar_match(
    match: MatchOdds, matches: Iterable[MatchOdds]
) -> MatchOdds | None:
    """Receive the most similar match by comparing home and away team names.
    Return:
        MatchOdds: Most similar match from the matches.
        None: There is no similar match.
    """

    str_temp = "{} | {}"

    most_similar = None
    most_similar_ratio = 0
    for m in matches:
        ratio = difflib.SequenceMatcher(
            None,
            str_temp.format(match.home_team, match.away_team),
            str_temp.format(m.home_team, m.away_team),
        ).ratio()

        if ratio < 0.50:
            continue

        if ratio > most_similar_ratio:
            most_similar = m
            most_similar_ratio = ratio

    return most_similar
