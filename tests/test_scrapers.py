import pytest

from src.scrapers import get_browser_context
from src.scrapers.supersport import get_supersport_odds


@pytest.fixture
async def page():
    async with get_browser_context() as c:
        yield await c.new_page()


async def test_get_supersport_odds(page):
    url = "https://supersportbet.com/sportsbook/soccer/german-bundesliga-209/"
    odds = await get_supersport_odds(page, url)
    assert len(odds) > 0
