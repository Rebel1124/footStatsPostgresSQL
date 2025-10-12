from datetime import UTC, datetime, tzinfo
from time import sleep
from zoneinfo import ZoneInfo

import parsel
from playwright import sync_api as playwright

from src.config import PINNACLE_URLS, League

from . import MatchOdds


class BlockedByWebsite(Exception):
    pass


def get_pinnacle_odds(
    page: playwright.Page,
    league: League,
) -> list[MatchOdds]:
    url = PINNACLE_URLS[league]
    if url is None:
        return []

    retries = 2

    def fail(reason: str):
        nonlocal retries
        if not retries:
            raise BlockedByWebsite(reason)
        retries -= 1

    while True:
        resp = page.goto(url, timeout=30_000, wait_until="commit")
        assert resp
        if resp.status != 200:
            fail(f"Status code {resp.status}")
            continue

        break

    page.wait_for_selector(".contentBlock.square", timeout=30_000)
    sleep(3)
    html = page.content()
    tz_str = page.evaluate("Intl.DateTimeFormat().resolvedOptions().timeZone")
    page.goto("about:blank")
    return list(_parse_odds(html, ZoneInfo(tz_str)))


def _parse_odds(html: str, browser_tz: tzinfo):
    root = parsel.Selector(html)
    [container] = root.css(".contentBlock.square")
    games = container.xpath("./div")

    games = iter(games)
    for game in games:
        if game.attrib["data-test-id"] == "Events.DateBar":
            [raw_date] = game.xpath("./span/text()").getall()
            game_date = datetime.strptime(raw_date, "%a, %b %d, %Y")
            next(games)  # skip next
            continue

        [element] = game.xpath(".//a/div/div")

        home_team, away_team, game_hours = element.xpath(".//text()").getall()
        hour, minute = game_hours.split(":")
        game_time = game_date.replace(
            hour=int(hour), minute=int(minute), tzinfo=browser_tz
        ).astimezone(UTC)

        home, draw, away, *_ = game.xpath(".//button//text()").getall()

        yield MatchOdds(
            home_team=home_team.removesuffix(" (match)"),
            away_team=away_team.removesuffix(" (match)"),
            home_odds=home,  # type: ignore
            draw_odds=draw,  # type: ignore
            away_odds=away,  # type: ignore
            start_at=game_time,
        )
