from collections.abc import Callable
from datetime import datetime
from typing import Any, Concatenate

import requests
from loguru import logger

from src.schemes import (
    BttsStats,
    Country,
    League,
    LeagueMatch,
    LeaguePlayer,
    LeagueReferee,
    LeagueStats,
    LeagueTables,
    LeagueTeam,
    Match,
    MatchDetails,
    Over25Stats,
    Team,
    TeamLastX,
)


class RetriesExceeded(Exception):
    pass


class NotFound(Exception):
    pass


class FootyStats:
    def __init__(self, api_key: str, max_attempts: int = 3):
        self.key = api_key
        self.max_attempts = max_attempts

    def get_countries(self) -> list[Country]:
        return self._get_all_data(self._get_countries)

    def get_leagues(self) -> list[League]:
        return self._get_all_data(self._get_leagues)

    def get_day_matches(self, day: datetime) -> list[Match]:
        return self._get_all_data(self._get_day_matches, day)

    def get_league_matches(self, season_id: int) -> list[LeagueMatch]:
        return self._get_all_data(self._get_league_matches, season_id)

    def get_league_teams(self, season_id: int) -> list[LeagueTeam]:
        return self._get_all_data(self._get_league_teams, season_id)

    def get_team(self, team_id: int) -> list[Team]:
        "Returns many states of the team."
        return self._get_all_data(self._get_team, team_id)

    def get_team_lastx(self, team_id: int) -> list[TeamLastX]:
        """Returns last 5/6/10 stats"""
        return self._get_all_data(self._get_team_lastx, team_id)

    def get_league_players(self, season_id: int) -> list[LeaguePlayer]:
        return self._get_all_data(self._get_league_players, season_id)

    def get_match_details(self, match_id: int) -> MatchDetails:
        [detail] = self._get_all_data(self._get_match_details, match_id)
        return detail

    def get_league_referees(self, season_id: int) -> list[LeagueReferee]:
        return self._get_all_data(self._get_league_referees, season_id)

    def get_league_stats(self, season_id: int) -> LeagueStats:
        [stats] = self._get_all_data(self._get_league_stats, season_id)
        return stats

    def get_league_tables(self, season_id: int) -> LeagueTables:
        [stats] = self._get_all_data(self._get_league_tables, season_id)
        return stats

    def get_over25_stats(self) -> Over25Stats:
        [stats] = self._get_all_data(self._get_over25_stats)
        return stats

    def get_btts_stats(self) -> BttsStats:
        [stats] = self._get_all_data(self._get_btts_stats)
        return stats

    # --- Inner ---

    def _get_league_stats(self, page: int, season_id: int):
        resp = requests.get(
            "https://api.football-data-api.com/league-season",
            {"key": self.key, "page": page, "season_id": season_id},
        )
        if resp.status_code == 417:
            raise NotFound(f"season_id={season_id}")

        resp.raise_for_status()
        body = resp.json()
        stats = [LeagueStats.model_validate(body["data"])]
        return stats, body

    def _get_league_tables(self, page: int, season_id: int):
        resp = requests.get(
            "https://api.football-data-api.com/league-tables",
            {"key": self.key, "page": page, "season_id": season_id},
        )
        if resp.status_code == 417:
            raise NotFound(f"season_id={season_id}")

        resp.raise_for_status()
        body = resp.json()
        stats = [LeagueTables.model_validate(body["data"])]
        return stats, body

    def _get_over25_stats(self, page: int):
        resp = requests.get(
            "https://api.football-data-api.com/stats-data-over25",
            {"key": self.key, "page": page},
        )

        resp.raise_for_status()
        body = resp.json()
        stats = [Over25Stats.model_validate(body["data"])]
        return stats, body

    def _get_btts_stats(self, page: int):
        resp = requests.get(
            "https://api.football-data-api.com/stats-data-btts",
            {"key": self.key, "page": page},
        )

        resp.raise_for_status()
        body = resp.json()
        stats = [BttsStats.model_validate(body["data"])]
        return stats, body

    def _get_match_details(self, page: int, match_id: int):
        resp = requests.get(
            "https://api.football-data-api.com/match",
            {"key": self.key, "page": page, "match_id": match_id},
        )
        if resp.status_code == 417:
            raise NotFound(f"match_id={match_id}")

        resp.raise_for_status()
        body = resp.json()
        stats = [MatchDetails.model_validate(body["data"])]
        return stats, body

    def _get_league_referees(self, page: int, season_id: int):
        resp = requests.get(
            "https://api.football-data-api.com/league-referees",
            {"key": self.key, "page": page, "season_id": season_id},
        )
        if resp.status_code == 417:
            raise NotFound(f"season_id={season_id}")

        resp.raise_for_status()
        body = resp.json()
        players = [LeagueReferee.model_validate(referee) for referee in body["data"]]
        return players, body

    def _get_league_players(self, page: int, season_id: int):
        resp = requests.get(
            "https://api.football-data-api.com/league-players",
            {"key": self.key, "page": page, "season_id": season_id, "include": "stats"},
        )
        if resp.status_code == 417:
            raise NotFound(f"season_id={season_id}")

        resp.raise_for_status()
        body = resp.json()
        players = [LeaguePlayer.model_validate(player) for player in body["data"]]
        return players, body

    def _get_league_teams(self, page: int, season_id: int):
        resp = requests.get(
            "https://api.football-data-api.com/league-teams",
            {"key": self.key, "page": page, "season_id": season_id, "include": "stats"},
        )
        if resp.status_code == 417:
            raise NotFound(f"season_id={season_id}")

        resp.raise_for_status()
        body = resp.json()
        teams = [LeagueTeam.model_validate(team) for team in body["data"]]
        return teams, body

    def _get_team(self, page: int, team_id: int):
        resp = requests.get(
            "https://api.football-data-api.com/team",
            {"key": self.key, "page": page, "team_id": team_id, "include": "stats"},
        )
        resp.raise_for_status()
        body = resp.json()
        teams = [Team.model_validate(team) for team in body["data"]]
        if not teams:
            raise NotFound(f"team_id={team_id}")
        return teams, body

    def _get_team_lastx(self, page: int, team_id: int):
        resp = requests.get(
            "https://api.football-data-api.com/lastx",
            {"key": self.key, "page": page, "team_id": team_id, "include": "stats"},
        )
        resp.raise_for_status()
        body = resp.json()
        teams = [TeamLastX.model_validate(team) for team in body["data"]]
        if not teams:
            raise NotFound(f"team_id={team_id}")
        return teams, body

    def _get_leagues(self, page: int):
        resp = requests.get(
            "https://api.football-data-api.com/league-list",
            {"key": self.key, "page": page},
        )
        resp.raise_for_status()
        body = resp.json()
        leagues = [League.model_validate(league) for league in body["data"]]
        return leagues, body

    def _get_day_matches(self, page: int, dt: datetime):
        resp = requests.get(
            "https://api.football-data-api.com/todays-matches",
            {"key": self.key, "page": page, "date": dt.strftime("%Y-%m-%d")},
        )
        resp.raise_for_status()
        body = resp.json()
        matches = [Match.model_validate(match) for match in body["data"]]
        return matches, body

    def _get_league_matches(self, page: int, season_id):
        resp = requests.get(
            "https://api.football-data-api.com/league-matches",
            {"key": self.key, "page": page, "season_id": season_id},
        )
        if resp.status_code == 417:
            raise NotFound(f"season_id={season_id}")

        resp.raise_for_status()
        body = resp.json()
        matches = [LeagueMatch.model_validate(match) for match in body["data"]]
        return matches, body

    def _get_countries(self, page: int):
        resp = requests.get(
            "https://api.football-data-api.com/country-list",
            {"key": self.key, "page": page},
        )
        resp.raise_for_status()
        body = resp.json()
        countries = [Country.model_validate(country) for country in body["data"]]
        return countries, body

    def _get_all_data[**P, T](
        self,
        get_data_and_body: Callable[
            Concatenate[int, P], tuple[list[T], Any]
        ],  # oh my god, this type actually works!
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> list[T]:
        left_attempts = self.max_attempts
        next_page = True
        data = []
        page = 1

        while next_page:
            if not left_attempts:
                raise RetriesExceeded(self.max_attempts)
            try:
                page_data, body = get_data_and_body(page, *args, **kwargs)
                next_page = body["pager"]["max_page"] > page
                data.extend(page_data)
            except NotFound:
                raise
            except Exception:
                left_attempts -= 1
                logger.opt(exception=True).warning(
                    "Failed to get data (left_attempts={left}/{total})",
                    left=left_attempts,
                    total=self.max_attempts,
                )
                continue

            left_attempts = self.max_attempts  # reset on each page
            page += 1

        return data
