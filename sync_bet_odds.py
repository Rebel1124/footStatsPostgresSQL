from loguru import logger

from src.config import League
from src.crud.match_bet_odds import upsert_matches_bet_odds
from src.db import get_db
from src.models import AggregatedMatchOdds
from src.scrapers.all import aggregate_match_odds, get_league_matches_odds


def main():
    logger.info("Starting syncing matches bet odds")

    odds: list[AggregatedMatchOdds] = []
    for league in League:
        try:
            matches = get_league_matches_odds(league)
            for match in aggregate_match_odds(matches, league):
                odds.append(match)
        except Exception:
            logger.exception(
                f"Failed to get matches bet odds for league {league.value}"
            )
        else:
            logger.info(f"Got matches bet odds for league {league.value}")

    if not odds:
        logger.warning("There are no matches bet odds to store in the database")
        return

    try:
        with get_db() as db:
            upsert_matches_bet_odds(db, odds)
            db.commit()
    except Exception:
        logger.exception("Failed to store scraped match bet odds in the database")
        return

    logger.success("Completed sync of match bet odds")


if __name__ == "__main__":
    main()
