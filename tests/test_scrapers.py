import pytest

from src.scrapers import get_browser_context, get_client
from src.scrapers.betway import get_betway_odds
from src.scrapers.supersport import get_supersport_odds


@pytest.fixture
async def client():
    async with get_client() as c:
        yield c


async def test_get_supersport_odds(client):
    url = "https://supersportbet.com/sportsbook/soccer/german-bundesliga-209/"
    odds = await get_supersport_odds(client, url)
    assert odds


async def test_get_betway_odds(client):
    urls = [
        "https://new.betway.co.za/sport/soccer?sortOrder=League&selectedLeagues=germany_bundesliga",
        # "https://new.betway.co.za/sport/soccer?sortOrder=League&selectedLeagues=international-clubs_uefa-champions-league",
        "https://new.betway.co.za/sport/soccer?sortOrder=League&selectedLeagues=england_premier-league",
        "https://new.betway.co.za/sport/soccer?sortOrder=League&selectedLeagues=england_championship",
        "https://new.betway.co.za/sport/soccer?sortOrder=League&selectedLeagues=spain_la-liga",
        "https://new.betway.co.za/sport/soccer?sortOrder=League&selectedLeagues=france_ligue-1",
        "https://new.betway.co.za/sport/soccer?sortOrder=League&selectedLeagues=italy_serie-a",
        "https://new.betway.co.za/sport/soccer?sortOrder=League&selectedLeagues=south-africa_premiership",
        "https://new.betway.co.za/sport/soccer?sortOrder=League&selectedLeagues=international-clubs_uefa-europa-league",
    ]
    for url in urls:
        odds = await get_betway_odds(client, url)
        assert odds, url
