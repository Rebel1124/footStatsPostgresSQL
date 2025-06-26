import pytest

from src.config import FOOTYSTATS_API_KEY
from src.footystats import FootyStats
from src.footystats_db import (
    LeaguesNotFound,
    get_season_metadatas,
)


def test_get_season_metadatas():
    footy = FootyStats(FOOTYSTATS_API_KEY, 2)
    seasons = get_season_metadatas(footy, {"Germany Bundesliga"}, 5)
    assert len(seasons) == 5 * 1
    assert seasons[0].league_name == "Germany Bundesliga"


def test_get_season_metadatas__not_found():
    footy = FootyStats(FOOTYSTATS_API_KEY, 2)
    with pytest.raises(LeaguesNotFound):
        get_season_metadatas(footy, {"Germany Bundesliga", "fk", "hello"})
