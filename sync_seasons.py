from loguru import logger

from src.config import FOOTYSTATS_API_KEY, LEAGUES_NAMES
from src.footystats import FootyStats
from src.footystats_db import (
    get_season_metadatas,
    upsert_season_to_db,
)
from src.utils import fetch_season


def sync_seasons():
    footy = FootyStats(FOOTYSTATS_API_KEY, 3)
    season_metadatas = get_season_metadatas(footy, LEAGUES_NAMES, last=1)
    for metadata in season_metadatas:
        season = fetch_season(footy, metadata)
        upsert_season_to_db(season)
        logger.info("Fetched and stored season (id={id})", id=season.season_id)


if __name__ == "__main__":
    sync_seasons()
