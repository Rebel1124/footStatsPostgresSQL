import os
import time

from loguru import logger

from src.config import FOOTYSTATS_API_KEY
from src.footystats import FootyStats
from src.footystats_db import (
    get_season_metadata_by_id,
    upser_match_details_to_db,
    upsert_season_to_db,
    upsert_team_to_db,
)
from src.utils import fetch_season

SEASOND_ID = int(os.environ["SEASON_ID"])
SECONDS_GAP = float(os.environ.get("SECONDS_GAP", 2))


def sync():
    footy = FootyStats(FOOTYSTATS_API_KEY, 3)
    metadata = get_season_metadata_by_id(footy, SEASOND_ID)
    if metadata is None:
        raise ValueError(f"Season not found (season_id={SEASOND_ID})")

    season = fetch_season(footy, metadata)
    upsert_season_to_db(season)
    logger.info("Fetched and stored season (id={id})", id=season.season_id)

    matches = footy.get_league_matches(metadata.season_id)
    for match in matches:
        time.sleep(SECONDS_GAP)
        match_details = footy.get_match_details(match.id)
        upser_match_details_to_db(match_details)
        upser_match_details_to_db(match_details)
        logger.info(
            "Fetched and stored match details (match_id={match_id}, season_id={season_id})",
            match_id=match.id,
            season_id=metadata.season_id,
        )

    teams = footy.get_league_teams(metadata.season_id)
    for team in teams:
        time.sleep(SECONDS_GAP)
        team_lastx = footy.get_team_lastx(team.id)
        team_snapshots = footy.get_team(team.id)
        upsert_team_to_db(team_snapshots, team_lastx)
        logger.info(
            "Fetched and stored team (team_id={team_id}, season_id={season_id})",
            team_id=team.id,
            season_id=metadata.season_id,
        )


if __name__ == "__main__":
    sync()
