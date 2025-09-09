import ssl
from contextlib import contextmanager
from enum import Enum
from time import sleep
from typing import Annotated

import httpx
from loguru import logger
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
from pydantic import AwareDatetime, BaseModel, StringConstraints

from src.config import CHROMIUM_PATH

type StrTeamName = Annotated[
    str,
    StringConstraints(
        min_length=2, strip_whitespace=True, max_length=100, to_lower=True
    ),
]


class Bookmaker(Enum):
    SUPER_SPORT_BET = "supersportbet.com"
    BET_WAY = "betway.co.za"
    HOLLYWOOD_BETS = "hollywoodbets.net"
    BET_10 = "10bet.co.za"
    SPORTING_BET = "sportingbet.co.za"
    SUPA_BETS = "supabets.co.za"


class MatchOdds(BaseModel):
    home_team: StrTeamName
    away_team: StrTeamName
    start_at: AwareDatetime

    home_odds: float
    draw_odds: float
    away_odds: float


HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7",
    # "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": '"Not)A;Brand";v="8", "Chromium";v="138"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "macOS",
    "Sec-Ch-Ua-Platform-version": "15.5.0",
    "Sec-Ch-Ua-Model": "",
    "Sec-Ch-Ua-Bitness": "64",
    "Sec-Ch-Ua-Full-Version-List": 'Not.A/Brand";v="99.0.0.0", "Chromium";v="136.0.7103.114"',
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


class RetryClient(httpx.Client):
    def send(self, request: httpx.Request, **kwargs):
        retries = 3

        while True:
            try:
                resp = super().send(request, **kwargs)
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

            sleep(2)


@contextmanager
def get_http_client():
    with RetryClient(
        headers=HEADERS,
        follow_redirects=True,
        # proxy="http://localhost:8080",
        # verify=False,
        transport=httpx.HTTPTransport(ssl_context),
        timeout=10,
    ) as client:
        yield client


@contextmanager
def get_browser_context():
    with Stealth().use_sync(sync_playwright()) as p:
        browser = p.chromium.launch(
            executable_path=CHROMIUM_PATH,
            args=["--disable-gpu", "--no-sandbox", "--headless"],
            # proxy=ProxySettings(server="localhost:8080"),
        )
        context = browser.new_context()

        yield context
