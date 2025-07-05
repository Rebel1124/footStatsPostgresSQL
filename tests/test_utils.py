import pytest

from src.config import FOOTYSTATS_API_KEY
from src.footystats import FootyStats
from src.footystats_db import (
    LeaguesNotFound,
    get_season_metadatas,
)


def test_get_season_metadatas():
    footy = FootyStats(FOOTYSTATS_API_KEY, 2)
    seasons = get_season_metadatas(footy, {"Germany Bundesliga"}, 3)
    assert len(seasons) == 3 * 1
    assert seasons[0].league_name == "Germany Bundesliga"

    assert {s.season_year for s in seasons} == {"2024/2025", "2023/2024", "2022/2023"}


def test_get_season_metadatas__not_found():
    footy = FootyStats(FOOTYSTATS_API_KEY, 2)
    with pytest.raises(LeaguesNotFound):
        get_season_metadatas(footy, {"Germany Bundesliga", "fk", "hello"})
