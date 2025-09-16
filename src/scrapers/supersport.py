from datetime import UTC, tzinfo
from zoneinfo import ZoneInfo

import parsel
from dateutil.parser import parse
from playwright import sync_api as playwright

from src.config import SUPER_SPORT_BET_URLS, League

from . import MatchOdds


class BlockedByWebsite(Exception):
    pass


def get_super_sport_bet_odds(
    page: playwright.Page,
    league: League,
) -> list[MatchOdds]:
    url = SUPER_SPORT_BET_URLS[league]
    if url is None:
        return []

    retries = 2

    def fail(reason: str):
        nonlocal retries
        if not retries:
            raise BlockedByWebsite(reason)
        retries -= 1

    while True:
        page.goto(url, timeout=60_000)

        title = page.locator("title").text_content()
        if title == "Access Restricted":
            fail("Access Restriction")
            continue

        block_headline = page.query_selector('h1[data-translate="block_headline"]')
        if block_headline:
            fail("Sorry, you have been blocked")
            continue

        break

    page.wait_for_selector(
        'section[data-app="EventsApp"]', timeout=90_000, state="attached"
    )
    html = page.content()
    tz_str = page.evaluate("Intl.DateTimeFormat().resolvedOptions().timeZone")
    print(tz_str)
    page.goto("about:blank")
    return list(parse_super_sport_odds(html, ZoneInfo(tz_str)))


def parse_super_sport_odds(html: str, browser_tz: tzinfo):
    root = parsel.Selector(html)
    containers = root.xpath("//section[@data-app='EventsApp']/div/div")
    games = containers[-1].xpath("./div[not(@class)]")

    for game in games:
        [raw_time] = game.xpath("./div[2]/p/text()").getall()
        if raw_time == "Live":
            continue

        home_team, away_team = game.xpath(".//a//span/text()").getall()
        home, draw, away, *_ = game.xpath(".//button//text()").getall()

        # be sure that datetime is initially UTC
        game_time = parse(raw_time).replace(tzinfo=browser_tz).astimezone(UTC)

        yield MatchOdds(
            home_team=home_team,
            away_team=away_team,
            home_odds=home,  # type: ignore
            draw_odds=draw,  # type: ignore
            away_odds=away,  # type: ignore
            start_at=game_time,
        )
