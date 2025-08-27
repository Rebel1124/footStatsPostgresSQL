
import parsel
from playwright.async_api import Page

from . import GameOdds


async def get_supersport_odds(page: Page, url: str) -> list[GameOdds]:
    await page.goto(url)
    html = await page.content()
    return list(parse_supersport_odds(html))


def parse_supersport_odds(html: str):
    [section] = parsel.Selector(html).xpath("//section[a[@title='Upcoming']]")
    [container] = section.xpath("./div/div")
    _, _, *games = container.xpath("./div")

    for game in games:
        home_team, away_team = game.xpath(".//a/p/span[1]//text()").getall()
        home, draw, away = game.xpath(".//button/span/span//text()").getall()

        yield GameOdds(
            home_team=home_team,
            away_team=away_team,
            home_odds=home,  # type: ignore
            draw_odds=draw,  # type: ignore
            away_odds=away,  # type: ignore
        )
