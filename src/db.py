from datetime import datetime
from typing import Annotated

from sqlalchemy import JSON, TIMESTAMP, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from src.config import DB_URL

engine = create_engine(DB_URL)
get_db = sessionmaker(engine)


def create_tables():
    with engine.connect() as conn:
        BaseDB.metadata.create_all(conn)
        conn.commit()


UpdatedAt = Annotated[datetime, mapped_column(TIMESTAMP(True))]


class BaseDB(DeclarativeBase):
    pass


class SeasonDB(BaseDB):
    __tablename__ = "footystats_seasons"

    season_id: Mapped[int] = mapped_column(primary_key=True)
    season_year: Mapped[str]
    league_name: Mapped[str]
    updated_at: Mapped[UpdatedAt]

    league_stats: Mapped[dict] = mapped_column(JSON)
    league_matches: Mapped[dict] = mapped_column(JSON)
    league_teams: Mapped[dict] = mapped_column(JSON)
    league_players: Mapped[dict] = mapped_column(JSON)
    league_referees: Mapped[dict] = mapped_column(JSON)
    league_tables: Mapped[dict] = mapped_column(JSON)

    updated_at: Mapped[UpdatedAt]


class MatchDetailsDB(BaseDB):
    __tablename__ = "footystats_match_details"

    match_id: Mapped[int] = mapped_column(primary_key=True)
    details: Mapped[dict] = mapped_column(JSON)

    updated_at: Mapped[UpdatedAt]


class TeamDB(BaseDB):
    __tablename__ = "footystats_teams"

    team_id: Mapped[int] = mapped_column(primary_key=True)
    team_last_x: Mapped[list[dict] | None] = mapped_column(JSON)
    team_snapshots: Mapped[list[dict]] = mapped_column(JSON)

    updated_at: Mapped[UpdatedAt]


class StatsDB(BaseDB):
    __tablename__ = "footystats_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    btts_stats: Mapped[dict] = mapped_column(JSON)
    over25_stats: Mapped[dict] = mapped_column(JSON)

    updated_at: Mapped[UpdatedAt]
