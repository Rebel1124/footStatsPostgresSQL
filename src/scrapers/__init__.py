from contextlib import asynccontextmanager
from typing import Annotated

from httpx import AsyncClient
from playwright.async_api import async_playwright
from pydantic import BaseModel, StringConstraints

StrTeamName = Annotated[
    str, StringConstraints(min_length=2, strip_whitespace=True, max_length=50)
]


class GameOdds(BaseModel):
    home_team: StrTeamName
    away_team: StrTeamName

    home_odds: float
    draw_odds: float
    away_odds: float


HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": '"Not)A;Brand";v="8", "Chromium";v="138"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
}


@asynccontextmanager
async def get_client():
    async with AsyncClient(
        headers=HEADERS,
        follow_redirects=True,
        verify=False,
        proxy="http://localhost:8080",
    ) as client:
        yield client


@asynccontextmanager
async def get_browser_context():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(extra_http_headers=HEADERS)
        yield context
