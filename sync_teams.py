from loguru import logger

from src.config import FOOTYSTATS_API_KEY, LEAGUES_NAMES
from src.footystats import FootyStats
from src.footystats_db import (
    get_season_metadatas,
    upsert_team_to_db,
)


def sync_teams():
    footy = FootyStats(FOOTYSTATS_API_KEY, 3)
    season_metadatas = get_season_metadatas(footy, LEAGUES_NAMES, 1)
    for metadata in season_metadatas:
        teams = footy.get_league_teams(metadata.season_id)
        teams_ids = {team.id for team in teams}
        for team_id in teams_ids:
            team_lastx = footy.get_team_lastx(team_id)
            team_snapshots = footy.get_team(team_id)
            upsert_team_to_db(team_snapshots, team_lastx)
            logger.info(
                "Fetched and stored team (team_id={team_id}, season_id={season_id})",
                team_id=team_id,
                season_id=metadata.season_id,
            )


if __name__ == "__main__":
    sync_teams()
