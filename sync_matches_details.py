from loguru import logger

from src.config import FOOTYSTATS_API_KEY, LEAGUES_NAMES
from src.footystats import FootyStats
from src.footystats_db import (
    add_match_details_to_db,
    get_season_metadatas,
)


def sync_matches_details():
    footy = FootyStats(FOOTYSTATS_API_KEY, 3)
    season_metadatas = get_season_metadatas(footy, LEAGUES_NAMES, last=1)
    for metadata in season_metadatas:
        matches = footy.get_league_matches(metadata.season_id)
        match_ids = {m.id for m in matches}
        # missing_ids = get_missing_match_ids(match_ids)
        for match_id in match_ids:
            match_details = footy.get_match_details(match_id)
            add_match_details_to_db(match_details)
            logger.info(
                "Fetched and stored match details (match_id={match_id}, season_id={season_id})",
                match_id=match_id,
                season_id=metadata.season_id,
            )


if __name__ == "__main__":
    sync_matches_details()
