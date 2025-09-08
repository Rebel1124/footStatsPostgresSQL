import difflib
from collections import defaultdict
from collections.abc import Iterable
from datetime import UTC, datetime

import httpx
from loguru import logger
from playwright import sync_api as playwright

from src.config import (
    League,
)
from src.models import AggregatedMatchOdds, Odds1X2
from src.scrapers import Bookmaker, MatchOdds
from src.scrapers.bet10 import get_bet_10_odds
from src.scrapers.betway import get_bet_way_odds
from src.scrapers.hollywood import get_hollywood_bets_odds
from src.scrapers.sportingbet import get_sporting_bet_access_id, get_sporting_bet_odds
from src.scrapers.supabets import get_supa_bets_odds
from src.scrapers.supersport import get_super_sport_bet_odds


def aggregate_match_odds(odds: dict[Bookmaker, list[MatchOdds]], league: League):
    map: defaultdict[datetime, defaultdict[Bookmaker, list[MatchOdds]]] = defaultdict(
        lambda: defaultdict(list)
    )
    now = datetime.now(UTC)
    for bookmarker, matches in odds.items():
        for match in matches:
            if now <= match.start_at:
                map[match.start_at][bookmarker].append(match)

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

        for bookmarker, matches in map[match.start_at].items():
            similar_match = _get_most_similar_match(match, matches)
            if similar_match is None:
                logger.warning(f"No similar match found for {match} in {matches}")
                continue
            matches.remove(similar_match)  # optimization

            match_odds.odds[bookmarker] = Odds1X2(
                home=similar_match.home_odds,
                draw=similar_match.draw_odds,
                away=similar_match.draw_odds,
            )

        yield match_odds


def get_league_matches_odds(
    client: httpx.Client,
    page: playwright.Page,
    league: League,
    bookmakers: Iterable[Bookmaker] = Bookmaker,
):
    res: dict[Bookmaker, list[MatchOdds]] = {}
    access_id = get_sporting_bet_access_id(client)

    for bookmaker in bookmakers:
        try:
            match bookmaker:
                case Bookmaker.SUPER_SPORT_BET as b:
                    res[b] = get_super_sport_bet_odds(page, league)
                case Bookmaker.BET_WAY as b:
                    res[b] = get_bet_way_odds(client, league)
                case Bookmaker.HOLLYWOOD_BETS as b:
                    res[b] = get_hollywood_bets_odds(client, league)
                case Bookmaker.BET_10 as b:
                    res[b] = get_bet_10_odds(client, league)
                case Bookmaker.SPORTING_BET as b:
                    res[b] = get_sporting_bet_odds(client, league, access_id=access_id)
                case Bookmaker.SUPA_BETS as b:
                    res[b] = get_supa_bets_odds(client, league)
                case _:
                    raise ValueError(f"Not supported bookmaker {bookmaker}")
        except Exception as e:
            logger.opt(exception=e).warning(
                f"Failed to get bet odds for {bookmaker} {league}"
            )
            res[bookmaker] = []

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
