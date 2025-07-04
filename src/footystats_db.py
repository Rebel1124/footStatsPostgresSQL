from collections.abc import Iterable, Sequence
from datetime import UTC, datetime
from typing import NamedTuple

from sqlalchemy import sql

from src.db import MatchDetailsDB, SeasonDB, StatsDB, TeamDB, get_db
from src.footystats import FootyStats
from src.schemes import Season, SeasonMetaData
from src.schemes.btts_stats import BttsStats
from src.schemes.match_details import MatchDetails
from src.schemes.over25_stats import Over25Stats
from src.schemes.season import SeasonWithUpdateAt
from src.schemes.team import Team
from src.schemes.team_lastx import TeamLastX


class StatsTuple(NamedTuple):
    btts_stats: BttsStats
    over25_stats: Over25Stats
    updated_at: datetime


class MatchDetailsTuple(NamedTuple):
    match_details: MatchDetails
    updated_at: datetime


class TeamTuple(NamedTuple):
    team_snapshots: list[Team]
    team_last_x: list[TeamLastX] | None
    update_at: datetime


def get_season_from_db(season_id: int) -> SeasonWithUpdateAt | None:
    with get_db() as db:
        if season := db.get(SeasonDB, season_id):
            return SeasonWithUpdateAt.model_validate(season, from_attributes=True)


def upsert_season_to_db(season: Season) -> None:
    values = season.model_dump(mode="json", by_alias=True)
    values.update(updated_at=datetime.now(UTC))

    with get_db() as db:
        db.merge(SeasonDB(**values))
        db.commit()


class LeaguesNotFound(Exception):
    pass


def get_season_metadatas(
    footy: FootyStats, league_names: Iterable[str], last: int = 1
) -> list[SeasonMetaData]:
    league_names = set(league_names)
    leagues = footy.get_leagues()
    seasons: list[SeasonMetaData] = []
    for league in leagues:
        try:
            league_names.remove(league.name)
        except KeyError:
            continue

        for season in league.season[-last:]:
            if season.year is None:
                continue
            metadata = SeasonMetaData(
                season_id=season.id, season_year=season.year, league_name=league.name
            )
            seasons.append(metadata)

    if league_names:
        raise LeaguesNotFound(league_names)

    return seasons


def upsert_stats_in_db(btts: BttsStats, over_25: Over25Stats) -> None:
    model = StatsDB(
        id=0,
        btts_stats=btts.model_dump(mode="json"),
        over25_stats=over_25.model_dump(mode="json"),
        updated_at=datetime.now(UTC),
    )
    with get_db() as db:
        db.merge(model)
        db.commit()


def get_stats_from_db() -> StatsTuple:
    with get_db() as db:
        stats = db.get_one(StatsDB, 0)
        btts_stats = BttsStats.model_validate(stats.btts_stats)
        over25_stats = Over25Stats.model_validate(stats.over25_stats)
        return StatsTuple(btts_stats, over25_stats, stats.updated_at)


def get_match_details_from_db(match_id: int) -> MatchDetailsTuple | None:
    with get_db() as db:
        if match := db.get(MatchDetailsDB, match_id):
            match_details = MatchDetails.model_validate(match.details)
            return MatchDetailsTuple(match_details, match.updated_at)


def upser_match_details_to_db(match: MatchDetails) -> None:
    details = match.model_dump(mode="json", by_alias=True)

    with get_db() as db:
        db.merge(
            MatchDetailsDB(
                match_id=match.id, details=details, updated_at=datetime.now(UTC)
            )
        )
        db.commit()


def get_missing_match_ids(ids: Iterable[int]) -> set[int]:
    """Returns passed IDs that are not in the database."""
    sttm = sql.select(MatchDetailsDB.match_id).where(MatchDetailsDB.match_id.in_(ids))
    with get_db() as db:
        db_ids = set(db.scalars(sttm))
        return db_ids.symmetric_difference(ids)


def get_missing_team_ids(ids: Iterable[int]) -> set[int]:
    """Returns passed IDs that are not in the database."""
    sttm = sql.select(TeamDB.team_id).where(TeamDB.team_id.in_(ids))
    with get_db() as db:
        db_ids = set(db.scalars(sttm))
        return db_ids.symmetric_difference(ids)


def upsert_team_to_db(
    team_snapshots: Sequence[Team], team_last_x: Iterable[TeamLastX] | None = None
) -> None:
    if len(team_snapshots) == 0:
        raise ValueError(
            "The passed team_snapshots argument sequence must have at least one item."
        )

    if team_last_x:
        team_last_x_dicts = [
            team.model_dump(mode="json", by_alias=True) for team in team_last_x
        ]
    else:
        team_last_x_dicts = None

    team_snaphosts_dicts = [
        team.model_dump(mode="json", by_alias=True) for team in team_snapshots
    ]

    with get_db() as db:
        db.merge(
            TeamDB(
                team_id=team_snapshots[0].id,
                team_last_x=team_last_x_dicts,
                team_snapshots=team_snaphosts_dicts,
                updated_at=datetime.now(UTC),
            )
        )
        db.commit()


def get_team_from_db(team_id: int) -> TeamTuple | None:
    with get_db() as db:
        if team := db.get(TeamDB, team_id):
            team_snapshots = [
                Team.model_validate(snapshot) for snapshot in team.team_snapshots
            ]
            if team.team_last_x is None:
                team_last_x = None
            else:
                team_last_x = [
                    TeamLastX.model_validate(last) for last in team.team_last_x
                ]
            return TeamTuple(team_snapshots, team_last_x, team.updated_at)
