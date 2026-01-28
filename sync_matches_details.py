import os
import time

from loguru import logger

from src.config import FOOTYSTATS_API_KEY, LEAGUES_NAMES
from src.footystats import FootyStats, NotFound
from src.footystats_db import (
    get_season_metadatas,
    upser_match_details_to_db,
)

SECONDS_GAP = float(os.environ["SECONDS_GAP"])


def sync_matches_details():
    footy = FootyStats(FOOTYSTATS_API_KEY, 3)
    season_metadatas = get_season_metadatas(footy, LEAGUES_NAMES, last=1)
    for metadata in season_metadatas:
        matches = footy.get_league_matches(metadata.season_id)
        match_ids = {m.id for m in matches}
        for match_id in match_ids:
            try:
                match_details = footy.get_match_details(match_id)
                upser_match_details_to_db(match_details)
                logger.info(
                    "Fetched and stored match details (match_id={match_id}, season_id={season_id})",
                    match_id=match_id,
                    season_id=metadata.season_id,
                )
            except NotFound as e:
                logger.warning(f"{e!r}")

            time.sleep(SECONDS_GAP)


if __name__ == "__main__":
    sync_matches_details()
