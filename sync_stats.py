from src.config import FOOTYSTATS_API_KEY
from src.footystats import FootyStats
from src.footystats_db import (
    upsert_stats_in_db,
)


def sync_stats():
    footy = FootyStats(FOOTYSTATS_API_KEY, 3)
    btts = footy.get_btts_stats()
    over25 = footy.get_over25_stats()
    upsert_stats_in_db(btts, over25)


if __name__ == "__main__":
    sync_stats()
