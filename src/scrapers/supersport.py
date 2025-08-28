from httpx import AsyncClient
import parsel
from playwright.async_api import Page

from . import GameOdds
from dateutil.parser import parse


async def get_supersport_odds(client: AsyncClient, url: str) -> list[GameOdds]:
    resp = await client.get(url)
    resp.raise_for_status()
    html = resp.content.decode()
    return list(parse_supersport_odds(html))


def parse_supersport_odds(html: str):
    [container] = parsel.Selector(html).xpath(
        "//div[./footer]/div[2]/section[2]/div/div"
    )
    _, _, *games = container.xpath("./div")

    for game in games:
        home_team, away_team = game.xpath(".//a//span/text()").getall()
        home, draw, away, *_ = game.xpath(".//button//text()").getall()
        [raw_time] = game.xpath("./div[2]/p/text()").getall()
        game_time = parse(raw_time)

        yield GameOdds(
            home_team=home_team,
            away_team=away_team,
            home_odds=home,  # type: ignore
            draw_odds=draw,  # type: ignore
            away_odds=away,  # type: ignore
            game_time=game_time,
        )
