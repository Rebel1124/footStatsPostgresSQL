import random
import ssl
from contextlib import contextmanager
from enum import Enum
from time import sleep
from typing import Annotated

import httpx
from loguru import logger
from playwright.sync_api import ProxySettings, sync_playwright
from pydantic import AwareDatetime, BaseModel, StringConstraints

from src.config import (
    CHROMIUM_PATH,
    HEADLESS_BROWSER,
    PROXY_PASSWORD,
    PROXY_URL,
    PROXY_USERNAME,
)

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
    PINNACLE = "pinnacle.com"


class MatchOdds(BaseModel):
    home_team: StrTeamName
    away_team: StrTeamName
    start_at: AwareDatetime

    home_odds: float | None
    draw_odds: float | None
    away_odds: float | None


HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7",
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

BROWSER_HEADERS = {
    "cache-control": "max-age=0",
    "sec-ch-ua": '"Chromium";v="139", "Not;A=Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-full-version": '"139.0.7258.156"',
    "sec-ch-ua-arch": '"arm"',
    "sec-ch-ua-platform": '"macOS"',
    "sec-ch-ua-platform-version": '"15.5.0"',
    "sec-ch-ua-model": '""',
    "sec-ch-ua-bitness": '"64"',
    "sec-ch-ua-full-version-list": '"Chromium";v="139.0.7258.156", "Not;A=Brand";v="99.0.0.0"',
    "dnt": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "navigate",
    "sec-fetch-user": "?1",
    "sec-fetch-dest": "document",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
}


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3


class RetryClient(httpx.Client):
    def send(self, request: httpx.Request, **kwargs):
        retries = 3

        while True:
            try:
                resp = super().send(request, **kwargs)
                logger.trace("{} -> {}", request, resp)
                return resp
            except httpx.RequestError as exc:
                if retries == 0:
                    raise exc
                logger.debug(
                    "Failed {} | Retries left {}",
                    request,
                    retries,
                )
                retries -= 1
                sleep(2)


@contextmanager
def get_http_client():
    if PROXY_URL:
        if PROXY_USERNAME and PROXY_PASSWORD:
            auth = (PROXY_USERNAME, PROXY_PASSWORD)
        else:
            auth = None
        proxy = httpx.Proxy(PROXY_URL, auth=auth)
    else:
        proxy = None

    with RetryClient(
        headers=HEADERS,
        follow_redirects=True,
        proxy=proxy,
        transport=httpx.HTTPTransport(ssl_context),
        timeout=10,
    ) as client:
        yield client


@contextmanager
def get_browser_context():
    with sync_playwright() as p:
        if PROXY_URL:
            proxy = ProxySettings(
                server=PROXY_URL,
                password=PROXY_PASSWORD,
                username=PROXY_USERNAME,
            )
        else:
            proxy = None
        browser = p.chromium.launch(
            headless=HEADLESS_BROWSER,
            executable_path=CHROMIUM_PATH,
            args=[
                "--disable-web-security",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-automation",  # Disables the automation flag
                "--disable-blink-features",  # Disables Blink features that might identify
                "--block-third-party-cookies",
            ],
            proxy=proxy,
        )
        context = browser.new_context(
            extra_http_headers=BROWSER_HEADERS,
            viewport={
                "height": random.randint(800, 1000),
                "width": random.randint(800, 1000),
            },
            locale="en-ZA",
            timezone_id="Africa/Johannesburg",
        )

        yield context
