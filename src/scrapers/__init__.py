from contextlib import asynccontextmanager
from datetime import datetime
from typing import Annotated, Literal
import ssl
import asyncio

import httpx
from playwright.async_api import async_playwright
from pydantic import BaseModel, StringConstraints
from loguru import logger

StrTeamName = Annotated[
    str, StringConstraints(min_length=2, strip_whitespace=True, max_length=50)
]


class GameOdds(BaseModel):
    home_team: StrTeamName
    away_team: StrTeamName

    home_odds: float
    draw_odds: float
    away_odds: float

    game_time: datetime


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


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3  # satisfy supersport bet


class RetryAsyncClient(httpx.AsyncClient):
    async def send(self, request: httpx.Request, **kwargs):
        retries = 3

        while True:
            try:
                resp = await super().send(request, **kwargs)
                logger.trace("{} -> {}", request, resp)
                return resp
            except httpx.RequestError:
                if retries == 0:
                    raise
                logger.debug(
                    "Failed {} | Retries left {}",
                    request,
                    retries,
                )
                retries -= 1

            await asyncio.sleep(3)


@asynccontextmanager
async def get_client():
    async with RetryAsyncClient(
        headers=HEADERS,
        follow_redirects=True,
        # proxy="http://localhost:8080",
        transport=httpx.AsyncHTTPTransport(ssl_context),
        timeout=10,
    ) as client:
        yield client


@asynccontextmanager
async def get_browser_context():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(extra_http_headers=HEADERS)
        yield context
