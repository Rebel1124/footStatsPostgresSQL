from collections.abc import Container
from datetime import UTC, datetime, timedelta

from src.footystats import FootyStats
from src.schemes.season import Season, SeasonMetaData


def fetch_season(footy: FootyStats, season: SeasonMetaData) -> Season:
    teams = footy.get_league_teams(season.season_id)
    stats = footy.get_league_stats(season.season_id)
    matches = footy.get_day_matches(datetime.today())
    matches = footy.get_league_matches(season.season_id)
    players = footy.get_league_players(season.season_id)
    referees = footy.get_league_referees(season.season_id)
    tables = footy.get_league_tables(season.season_id)

    return Season(
        season_id=season.season_id,
        season_year=season.season_year,
        league_name=season.league_name,
        league_stats=stats,
        league_matches=matches,
        league_teams=teams,
        league_players=players,
        league_referees=referees,
        league_tables=tables,
    )


def get_season_metadatas(
    footy: FootyStats, league_names: Container[str]
) -> list[SeasonMetaData]:
    leagues = footy.get_leagues()
    seasons: list[SeasonMetaData] = []
    for league in leagues:
        if league.name not in league_names:
            continue

        for season in league.season[-5:]:
            season = SeasonMetaData(
                season_id=season.id, season_year=season.year, league_name=league.name
            )
            seasons.append(season)

    return seasons


EPOCH = datetime(1, 1, 1, 0, 0, 0, tzinfo=UTC)


def ticks_to_datetime(ticks: int):
    seconds = ticks // 10_000_000
    return EPOCH + timedelta(seconds=seconds)


def datetime_to_ticks(dt: datetime):
    time_diff = dt - EPOCH
    seconds = time_diff.total_seconds()
    ticks = int(seconds * 10_000_000)
    return ticks
